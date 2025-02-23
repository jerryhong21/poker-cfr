from configparser import InterpolationSyntaxError
from game import Game, GameActions as GA
from create_charts import create_table
from cfr import CFR
import matplotlib.pyplot as plt
import json


def format_action_string(actions):
    action_string = []
    for action in actions:
        if action == GA.FOLD:
            action_string.append("FOLD")
        elif action == GA.CALL:
            action_string.append("CALL")
        elif action == GA.CHECK:
            action_string.append("CHECK")
        elif action == GA.BET:
            action_string.append("RAISE")
    return action_string


def format_infoset(infoset):
    print("Player Hand:", infoset[0:2])
    print("Action taken:", format_action_string(infoset[2:]))


def format_percentage(decimal_value):
    percentage = decimal_value * 100
    return f"{percentage:.2f}%"


def format_strategy(strategy_set):
    strategies = {}
    for strat in strategy_set:
        if strat == GA.FOLD:
            strategies["FOLD"] = format_percentage(strategy_set[strat])
        elif strat == GA.CALL:
            strategies["CALL"] = format_percentage(strategy_set[strat])
        elif strat == GA.CHECK:
            strategies["CHECK"] = format_percentage(strategy_set[strat])
        elif strat == GA.BET:
            strategies["RAISE"] = format_percentage(strategy_set[strat])
    return strategies


def main():
    try:
        iterations = int(input("Enter the number of iterations for the simulation: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    # Define bet amounts
    bet1 = 2
    bet2 = 8

    # Create and train the CFR model
    model = CFR()
    util = model.training(iterations, bet1, bet2)
    game_state = model.game_state_map_
    count = 0

    # Process each infoset in the game state
    for infoset in game_state:
        if len(infoset) == 4:
            node = game_state[infoset]
            strategy = node.getAverageStrategy()
            format_infoset(infoset)
            print(f"Encountered {node.timesEncountered_} times")
            print(f"Strategy: {format_strategy(strategy)}\n")
        count += 1

    # Generate strategy overview and save to JSON file
    # strategy_map = model.getStrategyOverview()
    # with open("strategy_charts/strategy.json", "a") as stream:
    #     print(json.dumps(strategy_map), file=stream)

    # # Create charts based on strategy decisions
    # for decision in strategy_map:
    #     table = create_table(decision, strategy_map[decision], iterations)

    print(f"In total, this simulation explored {count} decision nodes in the game")
    print(f"The utility was {util}")


if __name__ == "__main__":
    main()
