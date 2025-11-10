from .game import BlackjackGame

def simulate(strategy, num_rounds: int = 100000):
    game = BlackjackGame()
    results = [game.play_round(strategy) for _ in range(num_rounds)]
    wins = sum(1 for r in results if r == 1 or r == 1.5 or r == 2)
    losses = sum(1 for r in results if r == -1 or r == -2)
    pushes = results.count(0)
    return {
        "win_rate": wins / num_rounds,
        "loss_rate": losses / num_rounds,
        "push_rate": pushes / num_rounds,
    }
