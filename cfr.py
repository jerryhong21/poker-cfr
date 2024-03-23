from game import Game, GameActions as GA
import time

class CFR():

    # initialise game state 
    def __init__(self):
        # this map maps a history string -> nodes
        self.game_state_map_ = dict()

    def training(self, iterations, printInterval=1000000):
        util = 0.0  
        
        intervalStartTime = time.time()  
        for i in range(iterations):
            if i % printInterval == 0 and i != 0:
                intervalEndTime = time.time()  # End time of the current interval
                print(f"At iteration {i}, expected value is {util / i}")
                print(f"Time for last {printInterval} iterations: {intervalEndTime - intervalStartTime} seconds")
                intervalStartTime = time.time()  # Reset start time for the next interval

            cards = Game.dealCards(Game.DECK)
            history = ''
            util += self.cfr(cards, history, 1, 1)

        return util / iterations


    # determine available actions given history
    def GetPotentialActions(actions):
        potentialActions = []
        if (len(actions) == 0):
            return [GA.BET, GA.CHECK]
        lastAction = actions[-1]
        # determining
        if lastAction == GA.BET:
            # print('accessed1\n')
            potentialActions = [GA.CALL, GA.FOLD]
        elif lastAction == GA.CHECK and len(actions) < 2:
            # print('accessed2\n')
            potentialActions = [GA.CHECK, GA.BET]

        return potentialActions
    

    def isTerminal(self, history):
        if len(history) < 2:
            return False
        lastAction = history[-1]
        if lastAction == GA.CHECK or lastAction == GA.FOLD or lastAction == GA.CALL:
            return True

    # counts how many bets have been placed
    def countBetsAndCallsInHistory(self, history):
        return history.count(GA.BET) + history.count(GA.CALL)
    
    # counts the reward for winning player
    def getPotSize(self, history, anteSize = 1):
        return 2 * anteSize + self.countBetsAndCallsInHistory(history)
    
    # returns the appropriate payoff, 0 if tie
    def getPayoff(self, cards, activePlayer, oppPlayer, history):
        lastAction = history[-1]
        winner = Game.getWinner([cards[activePlayer], cards[oppPlayer]])
        # print(f"(Player {activePlayer + 1} active): Winner is {activePlayer+1 if winner == 1 and winner != 0 else oppPlayer + 1} ")
        # print(f"Active player has cards {cards[activePlayer]}, opp has {cards[oppPlayer]}")
        tie = True if winner == 0 else False
        activePlayerWins = True if winner == 1 else False

        if tie:
            return 0
        
        potSize = self.getPotSize(history, Game.ANTE)
        if lastAction == GA.CHECK or lastAction == GA.FOLD or lastAction == GA.CALL:
            return potSize if activePlayerWins else -potSize
        

    # recursive function, returns the expected node utility
    def cfr(self, cards, history, p1, p2):
        # print(cards)
        # print('history =' ,"'" + history + "'")
        rounds = len(history)
        # print("rounds =", str(rounds))
        activePlayer = rounds % 2
        oppPlayer = 1 - activePlayer

        infoset = cards[activePlayer][0] + cards[activePlayer][1] + history

        # base case: return payoff for terminal states
        if self.isTerminal(history):
            payoff = self.getPayoff(cards, activePlayer, oppPlayer, history)
            # print(f"At terminal node {infoset}, payoff = {payoff} as player {activePlayer + 1}")
            return payoff


        # create / infoset node using Node or game_state_map_
        if infoset not in self.game_state_map_:
            potentialActions = CFR.GetPotentialActions(history)
            node = Node(potentialActions)
            self.game_state_map_[infoset] = node
        else:
            node = self.game_state_map_[infoset]
            potentialActions = node.actions_
        node.timesEncountered_ += 1
    
        # iterative through each action and call cfr with additional history and probability
        realisationWeight = p1 if activePlayer == 0 else p2
        
        # retrive the indedent strategy profile for the node
        # sum of all strategies = 1
        strategy = node.GetStrategy(realisationWeight)
        nodeUtil = 0.0

        # records the utility of each action, utility is calculated through recursion
        util = {action: 0.0 for action in potentialActions}
        for potentialAction in potentialActions:
            historyNext = history + str(potentialAction)
            # print(f"At node {infoset}, historyNext = {historyNext}")
            # print("historyNext =",  "'" + historyNext+ "'")
            # calculating utility of action through recursive simulation until end of game
            if (activePlayer == 0):
                util[potentialAction] = - CFR.cfr(self, cards, historyNext, p1 * realisationWeight, p2)
                # negative value is to account for change of persepctive, since activePlayer changes at each recursion level
            else:
                util[potentialAction] = - CFR.cfr(self, cards, historyNext, p1, p2 * realisationWeight)

            # utility of the node is based on the utility of the next action * probability of next action 
            # utility next action is related the terminal payoff
            nodeUtil += (util[potentialAction] * strategy[potentialAction])


            # if len(infoset) == 4:
            #     print(nodeUtil)
        
        # print('Utility of node with infoset ', infoset, "is", nodeUtil)
        # iterative thorugh each action, compute and accumulate counterfactual regret
        for potentialAction in potentialActions:
            # calculating the regret for not taking the action
            # if utility of potential action is greater than the utility of this node, then regret is positive
            # this assesses decision quality, 
            regret = util[potentialAction] - nodeUtil

            
            # if len(infoset) == 4:
            #     print(util[potentialAction])
            #     # print(nodeUtil)
            #     print(f"At infoset {infoset}, regret for {potentialAction} is {regret}")
            #     print(f"Stategy = {strategy}")

            # cumulative regret is weighted by the probability that the opponent plays to the current infromation set
            # i.e. at the turn of potentialAction, activeplayer has changed
            # if the activePlayer right now is p1, then the chances of player 2 ACTUALISING the regret, is p2 (which is the change this decision gets to p2)
            node.regretSum_[potentialAction] += ((p2 if activePlayer == 0 else p1) * regret)

            # this resets regret so that it doesn't spiral towards a negative value all the time
            node.regretSum_[potentialAction] = 0 if node.regretSum_[potentialAction] < 0 else node.regretSum_[potentialAction]


        return nodeUtil


class Node():
    # numActions = len(Game.GA)
    def __init__(self, actions):
        self.util_ = 0.0
        self.actions_ = actions
        self.strategy_ = {action: 0.0 for action in actions}
        self.strategySum_ = {action: 0.0 for action in actions}
        self.regretSum_ = {action: 0.0 for action in actions}
        self.timesEncountered_ = 0
        self.isTerminalNode_ = False

    # Get current information set mixed strategy thorugh regret matching
    def GetStrategy(self, realisationWeight):

        # Normalise all strategies to 0 if regret is negative 
        # retain the ones with positive regret
        self.strategy_ = {action: (regret if regret > 0.0 else 0.0) for action, regret in self.regretSum_.items()}
        normalisingSum = sum(self.strategy_.values())

        # normalising all strategies such that all strategies sum to 1
        for action in self.actions_:
            if (normalisingSum > 0):
                self.strategy_[action] /= normalisingSum
            else:
                self.strategy_[action] = (1 / len(self.actions_))
            self.strategySum_[action] += (realisationWeight * self.strategy_[action])
        
        return self.strategy_

    # Get overall strategy at the node - supposed to be the strategy closest to Nash Equilibrium
    def getAverageStrategy(self):
        averageStrategy = {action: 0.0 for action in self.actions_}
        normalisingSum = sum(self.strategySum_.values())
        for action in self.actions_:
            averageStrategy[action] = (self.strategySum_[action] / normalisingSum) if normalisingSum > 0 else (1 / len(self.actions_))
        
        return averageStrategy
    