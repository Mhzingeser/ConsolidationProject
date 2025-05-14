import os
import random
import json #This is for the save system 
from typing import List, Dict, Optional, Protocol  #These will be needed for their selective-
#purposes, such as Listing cards on hand, options, protocol (for computer player).
import time
from datetime import timedelta
#I am adding a way to track game time.


# Card Section

class Card: ## Peer Editor (Arnab Sanyal): Aren't classes considered to be anti-patterns?
    def __init__(self, suit: str, rank: str):  #We will need a constructor for these in order to call on a specific function for the card
        self.suit = suit
        self.rank = rank
        #Intializes the cards of each type
    
    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
        #This is meant to return a fine printed string

    def __repr__(self) -> str:
        return f"Card('{self.suit}', '{self.rank}')"
    
    @property ## Peer Editor (Arnab Sanyal): What does this do?
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
        #Gives cards to players

    def reveal_card(self) -> Optional[Card]:
        if self.cards:
            card = self.cards.pop()
            self.discard_pile.append(card)
            return card
        return None
        #Once round is over, it shows what card is there
    
#AI Components

class AIStrategy(Protocol):
    def choose_card(self, hand: List[Card], lead_suit: Optional[str]) -> Card:
        ...  
        #... its meants to pass nothing from the start of initialization, its a premade template for the AI to use in order to do a function.

class BaseStrategy:
    def choose_card(self, hand: List[Card], lead_suit: Optional[str]) -> Card:
        suit_cards = [card for card in hand if card.suit == lead_suit] if lead_suit else []
        if suit_cards:
            return min(suit_cards, key = lambda c: c.value) 
            #lamda is a anonymous function and can take a number of arguments
        return random.choice(hand)

#Player Component

class Player:
    def __init__(self, name: str, is_computer: bool = False, strategy: Optional[AIStrategy] = None):
        self.name = name
        self.hand: List[Card] = []
        self.points = 0
        self.is_computer = is_computer
        self.strategy = strategy or BaseStrategy()
        self.total_turn_time = 0.0  # Track cumulative turn time in seconds
        self.turn_start_time = 0.0   # Track when turn begins
        #Initalizes the player of type human or computer. Gives both a list, and points to track

    def add_to_hand(self, cards: List[Card]):
        self.hand.extend(cards)

    def has_suit(self, suit: str) -> bool:
        return any(card.suit == suit for card in self.hand)

    def play_card(self, lead_suit: Optional[str] = None) -> Card:
        self.turn_start_time = time.time()  # Start timing
        
        if self.is_computer:
            # Add small delay to make computer feel more natural
            time.sleep(0.5)
            card = self.strategy.choose_card(self.hand, lead_suit)
        else:
            card = self._prompt_card_choice(lead_suit)

        turn_duration = time.time() - self.turn_start_time
        self.total_turn_time += turn_duration
        print(f"{self.name}'s turn took {turn_duration:.1f} seconds")
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
            print("Invalid choice. Try again. Please check spelling, no need to check for capitalization")


#Save Aspect
#This is needed if you want to track your win/loss ratio with the computer opponent
class GameStats:
    STATS_FILE = "tricksy_battle_stats.json"

    def __init__(self):
        self.stats = self._load_stats()
        # Add new timing stats
        self.stats.setdefault("total_game_time", 0.0)
        self.stats.setdefault("human_turn_time", 0.0)
        self.stats.setdefault("computer_turn_time", 0.0)
        self.stats.setdefault("average_turn_time", 0.0)

    def _load_stats(self) -> Dict:
        try:
            if os.path.exists(self.STATS_FILE):
                with open(self.STATS_FILE, 'r') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError):
            pass
        return {"games_played": 0, "human_wins": 0, "computer_wins": 0, "shot_the_moon": 0}

    def save_stats(self):
        try:
            with open(self.STATS_FILE, 'w') as f:
                json.dump(self.stats, f)
        except IOError:
            print("Warning: Could not save game stats.")

    def record_game(self, human_won: bool, shot_the_moon: bool = False):
        self.stats["games_played"] += 1
        if human_won:
            self.stats["human_wins"] += 1
        elif human_won == False: ## Peer Editor (Arnab Sanyal): This works, but I would use an elif statement here for clarity (as you have two different 'alternative' conditions - computer wins and 'shoot the moon')
            self.stats["computer_wins"] += 1
        if shot_the_moon: ## Peer Editor (Arnab Sanyal): Same as above
            self.stats["shot_the_moon"] += 1
        self.save_stats()

    def display_stats(self):
        print("\nGame Statistics:")
        for k, v in self.stats.items(): ## Peer Editor (Arnab Sanyal): I think the item names 'k' and 'v' are a bit too generic
            if k.endswith("_time"):
                # Format time values nicely
                if k == "average_turn_time":
                    print(f"Average turn time: {v:.1f} seconds")
                else:
                    hours, remainder = divmod(v, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    print(f"Total {k.replace('_', ' ')}: {int(hours)}h {int(minutes)}m {int(seconds)}s")
            else:
                print(f"{k.replace('_', ' ').capitalize()}: {v}")


#Game Manager/Gameplay aspect

class TricksyBattleGame:
    def __init__(self):  
        self.deck = Deck()
        self.human = Player("You")
        self.computer = Player("Computer", is_computer=True)
        self.stats = GameStats() #Meant for saving the stats after game is done
        self.leader = None
        self.round = 0
        self.game_start_time = 0.0  # Add game timer
        #The game start initialization, where everyone is at 0 points, round is 0

    def setup_game(self):
        self.deck.shuffle()
        self.human.add_to_hand(self.deck.deal(8))
        self.computer.add_to_hand(self.deck.deal(8))
        self.leader = random.choice([self.human, self.computer])
        print(f"\n{self.leader.name} leads the first round.")

    def play_game(self):
        print("\nWelcome to Tricksy Battle!")
        self.game_start_time = time.time()  # Start game timer
        self.setup_game()
        while self.round < 16 and self.human.hand:
            self.play_round()
            input("\nPress Enter to continue...")
        self._end_game()

    def play_round(self):
        self.round += 1
        print(f"\n=== Round {self.round} ===")
        print(f"Score - You: {self.human.points}, Computer: {self.computer.points}")

        if self.leader == self.human:
            follower = self.computer
        else:
            follower = self.human

       ## follower = self.computer if self.leader == self.human else self.human ## Peer Editor (Arnab Sanyal): A bit confused about what the else statement does here
        print(f"\n{self.leader.name} lead(s).")
        lead_card = self.leader.play_card()
        print(f"{self.leader.name} played: {lead_card}")

        print(f"{follower.name}(r)('s) turn.")
        follow_card = follower.play_card(lead_card.suit)
        print(f"{follower.name} played: {follow_card}")

        if follow_card.suit == lead_card.suit:
            winner = self.leader if lead_card.value > follow_card.value else follower
        else:
            winner = self.leader

        winner.points += 1
        self.leader = winner
        print(f"{winner.name} win(s) the round!")

        if winner == self.computer:
            self._computer_trash_talk()

        if revealed := self.deck.reveal_card():
            print(f"Revealed card: {revealed}")
        self._maybe_replenish_hands()
        if self._check_early_end():
            self._end_game()

    def _maybe_replenish_hands(self):
        if len(self.human.hand) == 4 and len(self.computer.hand) == 4:
            if len(self.deck.cards) >= 8:
                print("Refilling deck...")
                self.human.add_to_hand(self.deck.deal(4))
                self.computer.add_to_hand(self.deck.deal(4))
                #This is called when the card threshold for each player (mainly looking at player) is 4 of less

    def _check_early_end(self) -> bool:
        h, c = self.human.points, self.computer.points
        if (h == 16 and c == 0) or (c == 16 and h == 0): 
            winner = self.human if h == 16 else self.computer
            winner.points = 17
            #Checks for shot the moon conditions
            print(f"\n{winner.name} shot the moon!")
            return True
        if (h >= 9 and c >= 1) or (c >= 9 and h >= 1):
            #If no longer possible to "shoot the moon", then it will check the other win condition of 9 points
            print("\nOne player reached 9 points and the other has at least 1. GameOver.") 
            return True
        return False

    def _end_game(self):
        #Handles the endgame

        # Calculate total game time
        total_time = time.time() - self.game_start_time
        minutes, seconds = divmod(total_time, 60)

        # Update stats with timing data
        self.stats.stats["total_game_time"] += total_time
        self.stats.stats["human_turn_time"] += self.human.total_turn_time
        self.stats.stats["computer_turn_time"] += self.computer.total_turn_time
        total_turns = self.round * 2  # Each round has 2 turns
        self.stats.stats["average_turn_time"] = (
            (self.human.total_turn_time + self.computer.total_turn_time) / total_turns
        )

        print("\n=== Game Over! ===")
        print(f"Game duration: {int(minutes)}m {int(seconds)}s")
        print(f"Your total thinking time: {self.human.total_turn_time:.1f}s")
        print(f"Computer's total thinking time: {self.computer.total_turn_time:.1f}s")
        print(f"Average turn time: {self.stats.stats['average_turn_time']:.1f}s")

        print(f"Final Score - You: {self.human.points}, Computer: {self.computer.points}")
        if self.human.points > self.computer.points:
            print("You win!")
            self.stats.record_game(True, self.human.points == 17)
        elif self.computer.points > self.human.points:
            print("Computer wins.")
            self.stats.record_game(False, self.computer.points == 17)
            self._computer_gloat_win() #Called after showing the computer points to show the Computer won
        else:
            print("It's a tie!")
            self.stats.record_game(False)
        self.stats.display_stats()
    
    def _computer_trash_talk(self): ## Peer Editor (Arnab Sanyal): This is really funny LOL
        taunts = [
            "Too easy.",
            "Did you mean to play that card?",
            "You sure you know how this game works?",
            "Classic human error.",
            "I'm just getting started.",
            "That was adorable.",
            "I see every move... before you even make it.",
            "Better put your thinking cap on.",
            "You should probably surrender now.",
            "Do you want a rematch already?",
            "I can't believe im playing against a player so mediocre",
            "LOL L + RATIO LOSER!!!!",
            "Your current location is 51.2763° N, 30.2219° E"
        ]
        print(f"Computer: {random.choice(taunts)}")

    def _computer_gloat_win(self):
        taunts = [
            "Too easy.",
            "I thought I was playing against another player, looks like I was playing against an easy bot",
            "GG EZ",
            "No need to retry, I will just win again",
            "Just quit the game",
            "You were the chosen one!",
            "Hehehe easy win"
        ]
        print(f"Computer: {random.choice(taunts)}")    

        
def main():
    game = TricksyBattleGame()
    game.play_game()

main()