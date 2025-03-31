from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

import random
import eval7  # Ensure eval7 is installed: pip install eval7

def monte_carlo_equity(my_cards, board_cards, iterations=500):
    """
    Estimate hand equity using Monte Carlo simulation.

    Build4Good Hold'em specifics:
      - Each player has 3 hole cards.
      - The final board has 4 cards.
    
    Parameters:
      my_cards (list[str]): Your 3 hole cards (e.g., ["Ah", "Kd", "Qs"])
      board_cards (list[str]): Already-dealt community cards (0 preflop, 2 on flop, or 4 final cards)
      iterations (int): Number of simulation iterations

    Returns:
      float: Estimated win probability (ties count as half a win)
    """
    full_deck = eval7.Deck()
    known_cards = [eval7.Card(card) for card in (my_cards + board_cards)]
    remaining_cards = [card for card in full_deck.cards if card not in known_cards]
    
    wins = 0
    ties = 0
    total = 0
    missing_board = 4 - len(board_cards)
    
    for _ in range(iterations):
        deck_sample = random.sample(remaining_cards, 3 + missing_board)
        opp_hole = deck_sample[:3]
        sim_board = board_cards[:]  # start with known board cards
        if missing_board > 0:
            sim_board += [str(card) for card in deck_sample[3:]]
        
        complete_board = [eval7.Card(card) for card in sim_board]
        my_hand = [eval7.Card(card) for card in my_cards] + complete_board
        opp_hand = opp_hole + complete_board
        
        my_value = eval7.evaluate(my_hand)
        opp_value = eval7.evaluate(opp_hand)
        
        if my_value > opp_value:
            wins += 1
        elif my_value == opp_value:
            ties += 1
        total += 1

    equity = (wins + ties * 0.5) / total
    return equity

class Player(Bot):
    """
    A Build4Good pokerbot that uses Monte Carlo simulation along with bet-sizing
    guidelines inspired by pro strategies.
    """

    def __init__(self):
        self.round_counter = 0

    def handle_new_round(self, game_state, round_state, active):
        self.round_counter += 1

    def handle_round_over(self, game_state, terminal_state, active):
        pass

    def get_action(self, game_state, round_state, active):
        """
        Decide an action based on Monte Carlo simulation and aggressive bet sizing.

        Guidelines based on PokerCode's article:
          - Preflop: If equity > 60%, raise aggressively with a bet size of ~2.5× the big blind.
          - Postflop: Raise if equity exceeds pot odds by at least 20 percentage points,
                      using a bet size of ~67% of the pot.
        """
        legal_actions = round_state.legal_actions()
        street = round_state.street  # 0 for preflop, 2 for flop, 4 for final round
        my_cards = round_state.hands[active]  # Your 3 hole cards
        board_cards = round_state.deck[:street]  # Board cards (0, 2, or 4 cards)
        my_pip = round_state.pips[active]
        opp_pip = round_state.pips[1-active]
        pot = sum(round_state.pips)
        continue_cost = opp_pip - my_pip
        
        # Estimate hand equity via Monte Carlo simulation.
        equity = monte_carlo_equity(my_cards, board_cards, iterations=500)
        
        # Calculate pot odds (the cost to call relative to the total pot post-call)
        pot_odds = continue_cost / (pot + continue_cost) if continue_cost > 0 else 0

        # --- Preflop Decision (3 hole cards, no board) ---
        if street == 0:
            if equity > 0.60:
                if RaiseAction in legal_actions:
                    min_raise, max_raise = round_state.raise_bounds()
                    # Aggressive sizing: ~2.5x the big blind.
                    desired_raise = int(BIG_BLIND * 2.5)
                    # Clamp the desired raise within allowed bounds.
                    desired_raise = max(min_raise, min(desired_raise, max_raise))
                    return RaiseAction(desired_raise)
                elif CheckAction in legal_actions:
                    return CheckAction()
            else:
                if continue_cost <= 10 or continue_cost <= pot * 0.1:
                    return CallAction()
                else:
                    return FoldAction()
        
        # --- Postflop Decision (board cards revealed) ---
        else:
            # Determine if our equity exceeds the pot odds by a 20% margin.
            if (equity - pot_odds) > 0.20:
                if RaiseAction in legal_actions:
                    min_raise, max_raise = round_state.raise_bounds()
                    # Bet sizing: use roughly 67% of the pot.
                    desired_raise = int(pot * 0.67)
                    desired_raise = max(min_raise, min(desired_raise, max_raise))
                    return RaiseAction(desired_raise)
                elif CheckAction in legal_actions:
                    return CheckAction()
            elif equity >= pot_odds:
                return CallAction()
            else:
                return FoldAction()

if __name__ == '__main__':
    run_bot(Player(), parse_args())