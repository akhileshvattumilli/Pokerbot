# Project Description

**23NPCs** is a poker-playing bot originally developed for the **Build4Good 2025 Pokerbot Challenge**, a hackathon-style competition hosted by Build4Good and inspired by the MIT Pokerbots framework.

This project implements a bot for **B4G Hold'em**, a custom variant of Texas Hold'em. The bot is designed to autonomously play thousands of hands, make strategic betting decisions, and maximize long-term profit under strict time constraints.

## B4G Hold'em Rules

- Each player is dealt **3 private cards**.
- The flop consists of **2 community cards**, followed by a betting round.
- Then, **2 more community cards** are revealed, followed by a final betting round.
- Standard [Texas Hold'em hand rankings](https://www.cardplayer.com/rules-of-poker/hand-rankings) are used to determine the winner.
- Betting occurs in **two rounds** instead of the usual three.

## Match Format

- Each match consists of **5,000 hands** between two bots.
- Both players start each hand with **500 chips**.
- **Small blind:** 5 chips  
  **Big blind:** 10 chips  
  (blinds alternate each hand)
- Chips reset to 500 after each hand, but **bankrolls are tracked cumulatively**.
- The bot with the highest total bankroll after all rounds wins.

## Time Limit

- Each bot has a total of **180 seconds** per match.
- Once the time runs out, the bot will automatically fold all future hands.

## Project Structure

- `engine.py` – Main game engine (do not modify).
- `config.py` – Match configuration parameters (can be modified).
- `bots/` – Contains bot implementations.
  - Each bot lives in its own subfolder.
  - Includes a required `skeleton/` folder with essential base code (should not be edited).
- `player_chatbot/` – CLI interface to play against your own bot (helpful for testing).

## Dependencies

- Python ≥ 3.5
- [eval7](https://pypi.org/project/eval7/) – Used for hand evaluation.
  ```bash
  pip install eval7
