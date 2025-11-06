from .cards import Deck
from .hand import hand_value

class BlackjackGame:
    def __init__(self, num_decks: int = 6):
        self.deck = Deck(num_decks)

    def play_round(self, player_strategy):
        player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]

        # Player turn
        while player_strategy.should_hit(player_hand, dealer_hand[0]):
            player_hand.append(self.deck.deal_card())
            if hand_value(player_hand) > 21:
                return -1  # player busts

        # Dealer turn
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deck.deal_card())

        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            return 1
        elif player_total < dealer_total:
            return -1
        else:
            return 0
