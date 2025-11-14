from blackjack.strategy import RandomStrategy, BasicStrategy
from blackjack.simulation import simulate

def main():
    strategy = RandomStrategy()
    stats = simulate(strategy, num_rounds=1000000)
    print(f"Win: {stats['win_rate']:.2%}, Loss: {stats['loss_rate']:.2%}, Push: {stats['push_rate']:.2%}")

if __name__ == "__main__":
    main()
