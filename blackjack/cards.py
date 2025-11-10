import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {str(i): i for i in range(2, 11)}
values.update({'J': 10, 'Q': 10, 'K': 10, 'A': 11})


class Deck:
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.cards = self._create_deck()
        random.shuffle(self.cards)

    def _create_deck(self):
        return [rank for rank in ranks for suit in suits] * self.num_decks

    def deal_card(self):
        if not self.cards:
            self.cards = self._create_deck()
            random.shuffle(self.cards)
        return self.cards.pop()
