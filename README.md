# 23NPCs Pokerbot

`23NPC` is a poker-playing bot originally developed for the **Build4Good 2025 Pokerbot Challenge**, a hackathon competition inspired by the MIT Pokerbots framework. The challenge involved building a bot that could compete in a modified version of Texas Hold'em called **B4G Hold'em**.

This repository includes our bot's implementation, which uses Monte Carlo simulations to estimate hand strength and makes decisions based on calculated equity and pot odds.

## Bot Strategy: Monte Carlo + Smart Betting

The `23NPCs` bot estimates its chance of winning using a **Monte Carlo simulation** of random opponent hands and board outcomes. Based on the estimated **equity**, the bot makes betting decisions using logic inspired by real-world professional strategies.

### Key Logic

- **Preflop**:
  - If estimated equity > 60%, raise aggressively (≈2.5× big blind).
  - If marginal, call small bets or fold to larger ones.

- **Postflop**:
  - Raise if equity exceeds pot odds by at least **20%**.
  - Raise sizing: ~67% of the current pot.
  - Call if equity ≥ pot odds; otherwise, fold.

The core equity calculation is handled by a custom `monte_carlo_equity` function, simulating hundreds of hands per decision for accurate win-rate estimates.

## B4G Hold'em Rules Summary

- Each player is dealt **3 private (hole) cards**.
- The community board reveals:
  - **2 cards (flop)**, followed by a betting round.
  - **2 additional cards**, then a final betting round.
- **Hand rankings** follow [Texas Hold'em standards](https://www.cardplayer.com/rules-of-poker/hand-rankings).
- Only **two rounds of betting** per hand.

## Match Format

- Matches are played over **5,000 hands** between two bots.
- Each hand:
  - Players start with **500 chips**.
  - **Small blind:** 5 chips  
    **Big blind:** 10 chips
  - Blinds alternate each hand.
  - Chips reset each hand; **cumulative bankroll** determines the winner.

## Time Constraints

- Each bot has a **180-second time budget** per match.
- Once time runs out, the bot will **auto-fold** all remaining hands.

## Project Structure

- `engine.py` – Main engine for running matches (do not edit).
- `config.py` – Match configuration (editable).
- `bots/23NPCs/` – Contains the 23NPCs bot implementation.
  - Based on a required `skeleton/` structure.
- `player_chatbot/` – Command-line interface for testing bots interactively.

## Dependencies

- Python ≥ 3.5
- [eval7](https://pypi.org/project/eval7/) – For poker hand evaluation
  ```bash
  pip install eval7
