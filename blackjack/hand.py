from .cards import values

def hand_value(hand):
    value = sum(values[card] for card in hand)
    num_aces = hand.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21
