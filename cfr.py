from game import Game, GameActions


class CFR():
    # determine winner

    # initialise game state 
    def __init__(self):
        # this map maps a history string -> nodes
        self.game_state_map_ = dict()

    # def training(self):

    # recursive function, returns the expected node utility
    def cfr(self, cards, history, p1, p2):
        rounds = len(history)
        activePlayer = rounds % 2
        oppPlayer = 1 - activePlayer
        # return payoff for terminal states 

        infoset = cards[activePlayer] + history
        # create / infoset node using Node or game_state_map_
        # iterative through each action and call cfr with additional history and probability
        # iterative thorugh each action, compute and accumulate counterfactual regret
        


class Node():
    # numActions = len(Game.GameActions)
    def __init__(self, actions):
        numActions = len(GameActions)
        self.util_ = 0.0
        self.actions_ = actions
        self.strategy_ = {action: 0.0 for action in actions}
        self.strategySum_ = {action: 0.0 for action in actions}
        self.regretSum_ = {action: 0.0 for action in actions}
        self.isTerminalNode_ = False

    # determine available actions given history
    def GetAction(self):
        history = self.history
        if (history[-1] == GameActions.FOLD or GameActions.CALL):
            self.isTerminalNode_ = True
        lastAction = history[-1]
        match lastAction:
            case GameActions.BET:
                self.actions_ = [GameActions.CALL, GameActions.FOLD]
            case GameActions.CHECK:
                if (len(history) < 2):
                    self.actions_ = [GameActions.CHECK, GameActions.BET]
                else:
                    self.isTerminalNode_ = True
    
    # Get current information set mixed strategy thorugh regret matching
    def GetStrategy(self, realisationWeight):
        if (self.isTerminalNode_):
            return
        
        # Normalise all strategies to 0 if regret is negative 
        # retain the ones with positive regret
        self.strategy_ = {action: (regret if regret > 0.0 else 0.0) for action, regret in self.regretSum_.item()}
        normalisingSum = sum(self.strategy_)

        # normalising all strategies such that all strategies sum to 1
        for action in self.actions_:
            if (normalisingSum > 0):
                self.strategy_[action] /= normalisingSum
            else:
                self.strategy_[action] = (1 / len(GameActions))
            self.strategySum_[action] += realisationWeight * self.strategy_[action]
        
        return self.strategy_

    
        
        



            
 






















