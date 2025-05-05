**Tricksy Battle**

'Tricksy Battle' is a two-player card game where you compete against a computer to win tricks and score points.

**Gameplay**

- The game uses a `48-card deck` (**NO KING CARDS**).
- Each player is dealt `8 cards` to start.
- A round consists of each player playing one card:
  - One player `leads` with any card.
  - The other player `must follow suit` if possible.
  - The higher card in the `lead suit` wins the round and scores a point.
  - You `lead` a round if you win the previous round. 
- After each round:
  - A random card from the deck is `revealed` (but not added to any hand).
  - If both players are down to 4 cards, 4 more cards are dealt.
- The player with the `most points after 16 rounds wins` — or sooner, if special win conditions are met:
  - `Shot the Moon`: One player wins 16–0 — they are awarded 17 points and win instantly.
  - `Early End`: Game ends early if one player reaches `9 points` and the other has at least 1.


- How the coder did it
  - Just pick a card that is allowed and if higher than use it, if special like a Ace then use it. 
  - And not try to destroy the computer player.

**AI Computer Opponent**

The computer follows a simple strategy:
- Tries to follow suit when required.
- Plays the `lowest card possible` when following suit.
- Plays a `random card` when no matching suit is available.
- Will trash talk if they win the rounds

**Features**

- Simple AI using a Strategy Pattern
- Input-based human interaction (terminal based)
  - Total games played
  - Human and computer win counts
  - Number of “shot the moon” wins

**How to Run/Requirement**

You must have **Python 3.x** installed.

1. Download the project
2. Preferred CTRL + A then SHIFT + ENTER to access to run the whole thing.
3. Run the game... and have fun?

**NOTE** THIS GAME IS PLAYED VIA THE TERMINAL ON YOUR IDE (IDE such as: `Visual Studio Code`)

Game file name should be `Game.py`


**Classes and their functions**
`Card`
  - This class is meant as the defining class for cards such as Jack of Spades, Diamonds, Queen, Hearts, etc. The values get initialized
  - It represents a single card.
`Deck`
  - Represents a deck of 48 cards. This handles shuffling/dealing. 
`AIStrategy`
  - This class is the basis of the AI function that leads to the Basic Strategy class
  - Controls how computer opponent will play cards
`Base Strategy`
  - This class has the AI choose randomly but on the basis of what 'suits' the card on hand.
  - (Refer to AIStrategy)
`Player` 
  - Represents the player/computer and their action, action options.
`GameStats`
  - This is where the game statistics go and when the game is over, the statistics are saved into a JSON. JSON is a way to save things into a file, its a text file that is in a non txt format.
`TricksyBattleGame`
  - The main honcho of the game, its the manager and handler of all the classes, utilizing all the functions within the classes such as the initialization of all classes and functions. 
  - Handles win conditions, shuffles, and other card functions. 