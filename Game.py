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
