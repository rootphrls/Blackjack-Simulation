# hand.py
# Deze functies bepalen de waarde van een hand in blackjack en controleren of iemand een blackjack heeft.

from .cards import values

def hand_value(hand):
    # Deze functie berekent de totale waarde van een hand in blackjack.
    total = 0
    aces = 0
    for card in hand:
        if card == 'A':
            aces += 1
            total += 11
        else:
            total += values[card]
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def is_blackjack(hand):
    # Controleert of de hand een blackjack is (twee kaarten die samen 21 vormen).
    return len(hand) == 2 and hand_value(hand) == 21
