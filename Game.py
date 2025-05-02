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
    
#AI Components

class AIStrategy(Protocol):
    def choose_card(self, hand: List[Card], lead_suit: Optional[str]) -> Card:
        ...  #... its meants to pass nothing from the start of initialization, its a premade template for the AI to use in order to do a function.


#Player Component
class Player:
    def __init__(self, name: str, is_computer: bool = False, strategy: Optional[AIStrategy] = None):
        self.name = name
        self.hand: List[Card] = []
        self.points = 0
        self.is_computer = is_computer
        self.strategy = strategy or BasicStrategy()

    def add_to_hand(self, cards: List[Card]):
        self.hand.extend(cards)

    def has_suit(self, suit: str) -> bool:
        return any(card.suit == suit for card in self.hand)

    def play_card(self, lead_suit: Optional[str] = None) -> Card:
        if self.is_computer:
            card = self.strategy.choose_card(self.hand, lead_suit)
        else:
            card = self._prompt_card_choice(lead_suit)
        self.hand.remove(card)
        return card

    def _prompt_card_choice(self, lead_suit: Optional[str]) -> Card:
        while True:
            print(f"\nYour hand: {', '.join(str(card) for card in self.hand)}")
            if lead_suit and self.has_suit(lead_suit):
                print(f"You must play a {lead_suit} card.")
            choice = input("Choose a card to play (e.g., 'Ace of Hearts'): ").strip()
            for card in self.hand:
                if str(card).lower() == choice.lower():
                    if lead_suit and self.has_suit(lead_suit) and card.suit != lead_suit:
                        print(f"Must follow suit with a {lead_suit} card!")
                        break
                    return card
            print("Invalid choice. Try again.")
