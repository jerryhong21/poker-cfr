# High-level pseudocode of the poker game simulation with strategy learning

1. Import necessary libraries
   - Import random for generating random numbers

2. Define the Game class
   - Define constants for player actions (BET, CALL, CHECK, FOLD)
   - Define RANKS and SUITS of cards
   - Generate a DECK of cards combining RANKS and SUITS
   - Define a static method to deal random cards to two players
   - Define a static method to deal biased cards favoring one player
   - Define a static method to compare two card ranks and return the higher rank

3. Define the CFR (Counterfactual Regret Minimization) class for strategy optimization
   - Initialize the game state dictionary
   - Define a method to simplify a player's hand to a more abstract representation
   - Define a method to determine the winner between two hands based on poker hand rankings
   - Define a training method to simulate games and update strategies based on outcomes
     - Use an incremental progress bar to track training progress
     - On each iteration, simulate a game by dealing cards and executing a series of actions (bets, checks, folds)
     - Use Counterfactual Regret Minimization to update strategies based on the outcome of each game
   - Define a method to retrieve the optimized strategy after training
     - Classify the optimized strategy into different player action ranges (betting, calling, raising)
     - Clean up the strategy to remove negligible probabilities
   - Define the Counterfactual Regret Minimization algorithm (CFR)
     - Calculate the utility of each possible action in a given game state
     - Update regrets based on the difference between the utility of the taken action and the best possible action
     - Adjust strategies based on accumulated regrets

4. Define the Node class representing a game state in the CFR algorithm
   - Initialize with possible actions, regret sums, strategies, and strategy sums
   - Define a method to calculate the current strategy based on regret sums
     - Normalize the strategy so probabilities sum to 1
     - Update the strategy sums based on the current strategy and realization weight
   - Define a method to calculate the average strategy from the accumulated strategy sums

# Note: The code applies the concepts of Counterfactual Regret Minimization (CFR) to train a model to find an optimal poker strategy through self-play.