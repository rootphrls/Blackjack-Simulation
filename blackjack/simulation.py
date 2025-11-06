from .game import BlackjackGame

def simulate(strategy, num_rounds: int = 1000):
    game = BlackjackGame()
    results = [game.play_round(strategy) for _ in range(num_rounds)]
    wins = results.count(1)
    losses = results.count(-1)
    pushes = results.count(0)
    return {
        "win_rate": wins / num_rounds,
        "loss_rate": losses / num_rounds,
        "push_rate": pushes / num_rounds
    }
