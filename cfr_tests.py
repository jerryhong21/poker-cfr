from game import Game
from cfr import CFR



model = CFR()
# print(model.training(100000))

# 500 million
# print(model.training(500000000))

util = model.training(1000000)
gameState = model.game_state_map_
count = 0
for infoset in gameState:
    if len(infoset) == 4:
        node = gameState[infoset]
        print(f"node {infoset} was encountered {node.timesEncountered_} times")
        print(f"Regrets: {node.regretSum_}")
        print(f"Strategy: {node.getAverageStrategy()}")
        print('\n')
    count += 1
        # print(gameState[infoset])
        # print(state)

print(f"In total, this simulation explored {count} decision nodes in the game\n The utility was {util}")
