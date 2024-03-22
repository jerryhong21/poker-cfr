from game import Game, GameActions as GA


class CFR():

    # initialise game state 
    def __init__(self):
        # this map maps a history string -> nodes
        self.game_state_map_ = dict()

    def training(self, iterations, printInterval = 100000):
        # util of the overall training, indicates the overall payoff
        util = 0.0
        for i in range(iterations):
            if i % printInterval == 0 and i != 0:
                print("At interval", i, "util is", util / i)

            cards = Game.dealCards(Game.DECK)
            history = ""
            util += self.cfr(cards, history, 1, 1)
        
        return util / iterations


    # determine available actions given history
    def GetPotentialActions(actions):
        potentialActions = []
        if (len(actions) == 0):
            return [GA.BET, GA.CHECK]
        lastAction = actions[-1]
        # determining
        match lastAction:
            case GA.BET:
                potentialActions = [GA.CALL, GA.FOLD]
            case GA.CHECK:
                if (len(actions) < 2):
                    potentialActions = [GA.CHECK, GA.BET]

        return potentialActions
    

    def isTerminal(self, history):
        if len(history) < 2:
            return False
        lastAction = history[-1]
        if lastAction == GA.CHECK or lastAction == GA.FOLD or lastAction == GA.CALL:
            return True

    # counts how many bets have been placed
    def countBetsInHistory(history):
        return history.count(GA.BET)
    
    # counts the reward for winning player
    def getPotSize(self, history, anteSize = 1):
        return 2 * (anteSize + self.countBetsInHistory(history))
    
    # returns the appropriate payoff, 0 if tie
    def getPayoff(self, cards, activePlayer, oppPlayer, history):
        lastAction = history[-1]
        winner = Game.getWinner([cards[activePlayer], cards[oppPlayer]])
        tie = True if winner == 0 else False
        activePlayerWins = True if winner == 1 else False

        if tie:
            return 0
        
        potSize = self.getPotSize(history, Game.ANTE)
        if lastAction == GA.CHECK or lastAction == GA.FOLD or lastAction == GA.CALL:
            return potSize if activePlayerWins else -potSize
        

    # recursive function, returns the expected node utility
    def cfr(self, cards, history, p1, p2):
        rounds = len(history)
        activePlayer = rounds % 2
        oppPlayer = 1 - activePlayer

        # base case: return payoff for terminal states
        if self.isTerminal(history):
            return self.getPayoff(cards, activePlayer, oppPlayer, history)

        infoset = cards[activePlayer][0] + cards[activePlayer][1] + history

        # create / infoset node using Node or game_state_map_
        if infoset not in self.game_state_map_:
            potentialActions = CFR.GetPotentialActions(history)
            node = Node(potentialActions)
            self.game_state_map_[infoset] = node
        else:
            node = self.game_state_map_[infoset]
            potentialActions = node.actions_
    
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
            # calculating utility of action through recursive simulation until end of game
            if (activePlayer == 0):
                util[potentialAction] = - CFR.cfr(self, cards, historyNext, p1 * realisationWeight, p2)
                # negative value is to account for change of persepctive, since activePlayer changes at each recursion level
            else:
                util[potentialAction] = - CFR.cfr(self, cards, historyNext, p1, p2 * realisationWeight)

            # utility of the node is based on the utility of the next action * probability of next action 
            # utility next action is related the terminal payoff
            nodeUtil += (util[potentialAction] * strategy[potentialAction])

        # iterative thorugh each action, compute and accumulate counterfactual regret
        for potentialAction in potentialActions:
            # calculating the regret for not taking the action
            # if utility of potential action is greater than the utility of this node, then regret is positive
            # this assesses decision quality, 
            regret = util[potentialAction] - nodeUtil

            # cumulative regret is weighted by the probability that the opponent plays to the current infromation set
            # i.e. at the turn of potentialAction, activeplayer has changed
            # if the activePlayer right now is p1, then the chances of player 2 ACTUALISING the regret, is p2 (which is the change this decision gets to p2)
            node.regretSum_[potentialAction] += ((p2 if activePlayer == 0 else p1) * regret)


        return nodeUtil


class Node():
    # numActions = len(Game.GA)
    def __init__(self, actions):
        numActions = len(GA)
        self.util_ = 0.0
        self.actions_ = actions
        self.strategy_ = {action: 0.0 for action in actions}
        self.strategySum_ = {action: 0.0 for action in actions}
        self.regretSum_ = {action: 0.0 for action in actions}
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
                self.strategy_[action] = (1 / len(GA))
            self.strategySum_[action] += (realisationWeight * self.strategy_[action])
        
        return self.strategy_

    # Get overall strategy at the node - supposed to be the strategy closest to Nash Equilibrium
    def getAverageStrategy(self):
        averageStrategy = [0.0] * len(self.actions_)
        normalisingSum = sum(self.strategySum_.values())
        for action in self.actions_:
            averageStrategy[action] = (self.strategySum_[action] / normalisingSum) if normalisingSum > 0 else (1 / len(self.actions_))
        
        return averageStrategy
        
    
        
        



            



















