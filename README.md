
# Simplified Poker AI with CFR

This project develops an AI model that learns to master a simplified version of poker through iterative self-play. The model uses the Counterfactual Regret Minimisation (CFR) algorithm to approach Nash Equilibrium, honing its decision-making process to achieve optimal play. The CFR algorithm evaluates decisions by analysing their "counterfactual regret," guiding the model to favor strategies that would have performed better in hindsight.

## Simplified Poker Rules

The AI is trained on a simplified version of poker with the following rules:

- Both players contribute an initial wager known as an "ante."
- Player 1 has the option to "check" or "raise."
  - If player 1 checks, player 2 can also check or raise.
    - If player 2 raises, player 1 can either call or fold.
      - If player 1 calls, a showdown is reached to determine the winner based on hand rankings.
      - If player 1 folds, player 2 wins the pot.
  - If player 1 raises, player 2 has the options to call, raise, or fold.
    - If player 2 raises, player 1 can then call or fold.
    - If player 2 calls, a showdown is reached.
    - If player 2 folds, player 1 wins the pot.

These rules create a structured sequence of play that demands strategic decision-making, making the game an ideal scenario for applying the CFR algorithm. By simplifying the rules of traditional poker, the AI can focus on the core aspects of betting strategies and hand strength evaluation.

## Implementation of CFR in Simplified Poker

In our simplified poker environment, CFR operates by simulating hands between two AI players, with each decision point representing a unique "information set." The AI's strategy at these information sets is updated as it gains more experience, with the model calculating and storing the regret values associated with each possible action. These values are used to adjust future strategies, aiming to reduce regret and improve decision-making in similar situations.

The AI considers all possible actions it could have taken at each information set and computes the regret for not having chosen the action with the highest utility. Over many iterations, the AI's strategy converges towards an equilibrium where, if played perfectly by both sides, neither player has anything to gain by deviating from their current strategy.

## Getting Started

To experiment with the AI and the CFR implementation:

1. Ensure Python is installed on your system.
2. Clone this repository and navigate to the project directory.
3. Run the main script to start the AI's training process. This process is preset to 1 million training iterations.

```bash
python3 cfr_tests.py
```

## Contributing

We invite contributions to enhance the simulation of the poker game, improve the AI's performance, and refine the CFR algorithm's implementation.

## License

This project is available under the MIT License - details can be found in the `LICENSE` file.

## Acknowledgements

We express gratitude to the researchers and practitioners in the fields of game theory and artificial intelligence, whose innovative works inspire projects like ours.

---

This README offers a detailed overview for those interested in the intersection of AI, game theory, and poker simulations. For an in-depth look at the CFR implementation and its application to this simplified poker model, please review the source code and the comments therein.
