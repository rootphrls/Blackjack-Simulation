# main_counting.py
# Een script om alles uit te voeren en statistieken in consol te kunnen zien.

from blackjack.strategy import BasicStrategy, RandomStrategy
from blackjack.simulation import simulate

def main():
    strategy = RandomStrategy()
    strategyName = strategy.__class__.__name__

    stats_basic = simulate(strategy, num_rounds=100000, use_counting=False, min_bet=1, init_bankroll=100000.0)
    print(f"{strategyName} (no counting)")
    print(f"Initial bankroll: {stats_basic['initial_bankroll']}")
    print(f"Final bankroll:   {stats_basic['final_bankroll']:.2f}")
    print(f"Avg return/round: {stats_basic['avg_return_per_round']:.5f}")
    print(f"Win/Loss/Push rates: {stats_basic['win_rate']:.3%}, {stats_basic['loss_rate']:.3%}, {stats_basic['push_rate']:.3%}")
    print()

    stats_count = simulate(strategy, num_rounds=100000, use_counting=True, min_bet=1, init_bankroll=100000.0)
    print(f"{strategyName} + 3-COUNT CARD COUNTING")
    print(f"Initial bankroll: {stats_count['initial_bankroll']}")
    print(f"Final bankroll:   {stats_count['final_bankroll']:.2f}")
    print(f"Avg return/round: {stats_count['avg_return_per_round']:.5f}")
    print(f"Win/Loss/Push rates: {stats_count['win_rate']:.3%}, {stats_count['loss_rate']:.3%}, {stats_count['push_rate']:.3%}")

if __name__ == "__main__":
    main()
