# simulation.py
# Deze module voert duizenden (num_rounds) rondes uit om gemiddelde winst/verlies te berekenen.

from .game import BlackjackGame
from .card_count import CardCounter
from typing import Optional

def simulate(strategy, num_rounds: int = 100000, use_counting: bool = False, min_bet: int = 1, init_bankroll: float = 1000.0):
    game = BlackjackGame()
    counter: Optional[CardCounter] = CardCounter(min_bet=min_bet) if use_counting else None

    bankroll = init_bankroll
    bankroll_history = []
    results_raw = []
    wins = losses = pushes = 0

    for _ in range(num_rounds):
        if counter:
            bet_units = counter.bet_size(game.deck)
            bet = bet_units
        else:
            bet = min_bet

        outcome = game.play_round(strategy, counter)

        if isinstance(outcome, (int, float)):
            money_change = outcome * bet
        else:
            if outcome == "bust":
                money_change = -1 * bet
            else:
                money_change = 0

        bankroll += money_change
        bankroll_history.append(bankroll)
        results_raw.append(money_change)

        if money_change > 0:
            wins += 1
        elif money_change < 0:
            losses += 1
        else:
            pushes += 1

    avg_return_per_round = sum(results_raw) / num_rounds

    return {
        "initial_bankroll": init_bankroll,
        "final_bankroll": bankroll,
        "avg_return_per_round": avg_return_per_round,
        "win_rate": wins / num_rounds,
        "loss_rate": losses / num_rounds,
        "push_rate": pushes / num_rounds,
        "bankroll_history": bankroll_history
    }
