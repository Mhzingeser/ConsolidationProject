import os
import random

from typing import List, Dict, Optional, Protocol  #These will be needed for their selective-
#purposes, such as Listing cards on hand, options, protocol (for computer player).


# Card Section

class Card:
    def __init__(self, suit: str, rank: str):    #We will need a constructor for these in order to call on a specific function for the card
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        return f"Card('{self.suit}', '{self.rank}')"
    
    @property
    def value(self) -> int:
        rank_values = {
            'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'Jack': 11, 'Queen': 12
        }
        return rank_values[self.rank]
    
class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, count: int) -> List[Card]:
        return [self.cards.pop() for _ in range(min(count, len(self.cards)))]

    def reveal_card(self) -> Optional[Card]:
        if self.cards:
            card = self.cards.pop()
            self.discard_pile.append(card)
            return card
        return None
