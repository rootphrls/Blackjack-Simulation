import random

# cards.py
# Dit bestand maakt het kaartspel aan.
# We gebruiken meerdere decks (zoals in een echt casino) en zorgen dat kaarten geschud en gedeeld worden.

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] # De vier soorten kaarten
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] # Mogelijke waarden
values = {str(i): i for i in range(2, 11)} # Kaarten 2-10 behouden hun numerieke waarde
values.update({'J': 10, 'Q': 10, 'K': 10, 'A': 11}) # Boeren, Vrouwen, Koningen zijn 10, Aas is 11 (of 1 indien nodig)


class Deck:
    # Dit functie initialiseert het deck met een bepaald aantal decks (standaard 6 in Holland Casino)
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.cards = self._create_deck()
        random.shuffle(self.cards)
        self.reshuffled = False

    def _create_deck(self):
        # Maakt een nieuw deck met het opgegeven aantal decks
        return [rank for rank in ranks for _ in suits] * self.num_decks

    def cards_left(self):
        # Geeft het aantal resterende kaarten in het deck
        return len(self.cards)

    def deal_card(self):
        # Deelt een kaart uit het deck, en schudt opnieuw als de penetratielimiet (cut card) is bereikt
        total_cards = 52 * self.num_decks
        penetration_limit = 0.25 * total_cards
        if len(self.cards) < penetration_limit:
            self.cards = self._create_deck()
            random.shuffle(self.cards)
            self.reshuffled = True
        else:
            self.reshuffled = False
        return self.cards.pop()
