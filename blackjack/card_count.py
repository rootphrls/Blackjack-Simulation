# card_count.py
# Hier implementeren wij kaartentellen en daarbij gebruiken wij 3-count systeem.
# Dit is meest nauwkeurige kaartentellensysteem.

from typing import Dict

class CardCounter:

    DEFAULT_WEIGHTS = {
        '2': +0.5, '3': +1, '4': +1, '5': +1.5, '6': +1,
        '7': +0.5, '8': 0, '9': -0.5, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
    }

    def __init__(self, weights: Dict[str, int] = None, min_bet: int = 1):
        self.weights = weights if weights is not None else dict(self.DEFAULT_WEIGHTS)
        self.running = 0
        self.min_bet = min_bet

        # Inzet wordt hier exponentieél verhoogd op basis van true count.
        self.bet_map = {
            -99: 1,
            1: 2,
            2: 4,
            3: 8,
            4: 12
        }

    def reset(self):
        # Reset de running count naar 0.
        self.running = 0

    def update(self, card: str):
        # Voeg de waarde van een geziene kaart toe aan de running count.
        if card not in self.weights:
            if card in ('T',):
                self.running += self.weights.get('10', 0)
            else:
                return
        else:
            self.running += self.weights[card]

    def true_count(self, deck):
        # Bereken de true count door de running count te delen door het aantal resterende decks.
        cards_left = deck.cards_left()
        decks_remaining = max(cards_left / 52.0, 0.0001)
        return self.running / decks_remaining

    def bet_size(self, deck):
        # Bepaal de inzet op basis van de true count.
        tc = int(self.true_count(deck))
        multiplier = max(1, 1 + tc)
        multiplier = min(multiplier, 12)
        return self.min_bet * multiplier
