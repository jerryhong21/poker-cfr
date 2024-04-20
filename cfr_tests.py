from configparser import InterpolationSyntaxError

from numpy import true_divide
from game import Game, GameActions as GA
from create_charts import create_table
from cfr import CFR
import matplotlib.pyplot as plt
import json

iterations = 10000000

model = CFR()
# print(model.training(100000))

# 500 million
# print(model.training(500000000))

def formatActionString(actions):
    actionString = []
    for action in actions:
        if action == GA.FOLD:
            actionString.append('FOLD')
        elif action == GA.CALL:
            actionString.append('CALL')
        elif action == GA.CHECK:
            actionString.append('CHECK')
        elif action == GA.BET:
            actionString.append('RAISE')
    return actionString

def formatInfoset(infoset):
    print("Player Hand: ", infoset[0:2])
    print("Action taken: ", formatActionString(infoset[2:]))

def formatPercentage(decimal_value):
    percentage = decimal_value * 100
    formattedPercentage = f"{percentage:.2f}%"
    return formattedPercentage
    
def formatStrategy(strategySet):
    strategies = dict()
    for strat in strategySet:
        if strat == GA.FOLD:
            strategies['FOLD'] = formatPercentage(strategySet[strat])
        elif strat == GA.CALL:
            strategies['CALL'] = formatPercentage(strategySet[strat])
        elif strat == GA.CHECK:
            strategies['CHECK'] = formatPercentage(strategySet[strat])
        elif strat == GA.BET:
            strategies['RAISE'] = formatPercentage(strategySet[strat])

    return strategies

bet1 = 2
bet2 = 8

util = model.training(iterations, bet1, bet2)
gameState = model.game_state_map_
count = 0
for infoset in gameState:
    if len(infoset) == 4:
        node = gameState[infoset]
        strategy = node.getAverageStrategy()
        formatInfoset(infoset)
        print(f"Encountered {node.timesEncountered_} times")
        # print(f"Regrets: {node.regretSum_}")
        print(f"Strategy: {formatStrategy(strategy)}")
        print('\n')
    count += 1
        # print(gameState[infoset])
        # print(state)

strategyMap = model.getStrategyOverview()
with open('strategy_charts/strategy.json', 'a') as stream:
    print(json.dumps(strategyMap), file=stream)
for decision in strategyMap:
    table = create_table(decision, strategyMap[decision], iterations)

print(f"In total, this simulation explored {count} decision nodes in the game\n The utility was {util}")
