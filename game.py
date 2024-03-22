import numpy as np
from enum import Enum
import random

class GameActions(Enum):
    BET = '0'
    CHECK = '1'
    CALL = '2'
    FOLD = '3'

class Game():

    RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    SUITS = ['h', 's', 'c', 'd']
    
    def initDeck(ranks, suits):
        DECK = [rank + suit for rank in ranks for suit in suits]
        return DECK
        
    @staticmethod
    def dealCards(deck):
        player1Cards = random.sample(deck, 2)
        updatedDeck = [card for card in deck if card not in player1Cards]
        player2Cards = random.sample(updatedDeck, 2)
        return player1Cards, player2Cards
    
deck = Game.initDeck(Game.RANKS, Game.SUITS)
print(Game.dealCards(deck))

print(deck)
count = 0
cards = Game.dealCards(deck)
# # this calculates how long it takes for both players to be dealt bullets
# # on average around 300,000 times 
# while not (cards[0][0][0] == 'A' and cards[0][1][0] == 'A' and cards[1][0][0] == 'A' and cards[1][1][0] == 'A'):
#     count += 1
#     # print(cards)
#     cards = Game.dealCards(deck)
# print(cards)
# print(count)
