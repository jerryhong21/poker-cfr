from enum import Enum
import random
from util import cmp

class GameActions():
    BET = '0'
    CHECK = '1'
    CALL = '2'
    FOLD = '3'
    ACTIONS = 4


class Game():

    def __init__(self):
        pass

    RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    SUITS = ['h', 's', 'c', 'd']
    ANTE = 1

    DECK = []

    # Initialising deck
    for rank in RANKS:
        for i in range(4):
            DECK.append(rank)
    # for rank in RANKS:
    #     for suit in SUITS:
    #         DECK.append(rank + suit)
        
    @staticmethod
    def dealCards(deck):
        player1Cards = random.sample(deck, 2)
        updatedDeck = [card for card in deck if card not in player1Cards]
        player2Cards = random.sample(updatedDeck, 2)
        return player1Cards, player2Cards

    # Returns 1 if card1 > card 2
    # Returns -1 if card2 > card1
    # Returns 0 if tie
    def determineCardRank(card1, card2):
        return cmp(Game.RANKS.index(card2[0]), Game.RANKS.index(card1[0]))
            
    def playerHasPair(card1, card2):
        return card1 == card2

    # Returns 1 if player 1 wins
    # Returns 2 if player 2 wins
    # Returns 0 if tie
    def getWinner(cards):
        player1Cards, player2Cards = cards
        
        player1HasPair = True if Game.playerHasPair(player1Cards[0], player1Cards[1]) else False
        player2HasPair = True if Game.playerHasPair(player2Cards[0], player2Cards[1]) else False
        
        # default tie
        winner = 0
        # if both of them have a pair -> highest card
        if (player1HasPair and player2HasPair):
            rank = Game.determineCardRank(player1Cards[0], player2Cards[0])
            if rank == 1: 
                winner = 1
            elif rank == -1:
                winner = 2
        # if one of them has a pair -> pair wins
        elif player1HasPair:
            winner = 1
        elif player2HasPair:
            winner = 2
        # if none of them have a pair -> high card wins
        elif (not player1HasPair and not player2HasPair):
            player1HighCard = player1Cards[0] if Game.determineCardRank(player1Cards[0], player1Cards[1]) == 1 else player1Cards[1]
            # print(player1HighCard)
            player2HighCard = player2Cards[0] if Game.determineCardRank(player2Cards[0], player2Cards[1]) == 1 else player2Cards[1]
            # print(player2HighCard)
            rank = Game.determineCardRank(player1HighCard, player2HighCard)
            if rank == 1:
                winner = 1
            elif rank == -1:
                winner = 2
        return winner

# print(Game.getWinner([['T','7'],['9','5']]))
# print(Game.determineCardRank('T', '7'))
# deck = Game.initDeck(Game.RANKS, Game.SUITS)
# print(Game.dealCards(deck))

# print(deck)
# count = 0
# cards = Game.dealCards(deck)
# # # this calculates how long it takes for both players to be dealt bullets
# # on average around 300,000 times 
# while not (cards[0][0][0] == 'A' and cards[0][1][0] == 'A' and cards[1][0][0] == 'A' and cards[1][1][0] == 'A'):
#     count += 1
#     # print(cards)
#     cards = Game.dealCards(deck)
# print(cards)
# print(count)

