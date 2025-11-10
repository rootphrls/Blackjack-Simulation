from .cards import Deck
from .hand import hand_value, is_blackjack


class BlackjackGame:
    def __init__(self, num_decks: int = 6):
        self.deck = Deck(num_decks)

    def play_round(self, player_strategy):
        player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        dealer_hand = [self.deck.deal_card()]

        if is_blackjack(player_hand):
            return 1.5

        result = self._play_hand(player_hand, dealer_hand, player_strategy)
        if result == "bust":
            return -1

        # Dealer draws now
        dealer_hand.append(self.deck.deal_card())
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deck.deal_card())

        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            return result
        elif player_total < dealer_total:
            return -abs(result)
        else:
            return 0

    def _play_hand(self, player_hand, dealer_hand, strategy):
        doubled = False
        while True:
            action = strategy.get_action(player_hand, dealer_hand[0])

            if action == "H":
                player_hand.append(self.deck.deal_card())
                if hand_value(player_hand) > 21:
                    return "bust"

            elif action == "S":
                break

            elif action in ("D", "Dp"):
                total = hand_value(player_hand)
                if total not in (9, 10, 11):  # Holland Casino Rule
                    action = "H"
                    continue
                doubled = True
                player_hand.append(self.deck.deal_card())
                if hand_value(player_hand) > 21:
                    return "bust"
                break

            elif action == "SP":
                return self._handle_split(player_hand, dealer_hand, strategy)

            else:
                break

        return 2 if doubled else 1

    def _handle_split(self, player_hand, dealer_hand, strategy):
        if len(player_hand) != 2 or player_hand[0] != player_hand[1]:
            return 1

        first = [player_hand[0], self.deck.deal_card()]
        second = [player_hand[1], self.deck.deal_card()]

        if player_hand[0] == 'A':
            # Only one card per Ace split
            return (self._finish_split_ace(first, dealer_hand, strategy) +
                    self._finish_split_ace(second, dealer_hand, strategy)) / 2

        res1 = self._play_hand(first, dealer_hand, strategy)
        res2 = self._play_hand(second, dealer_hand, strategy)

        res1 = -1 if res1 == "bust" else res1
        res2 = -1 if res2 == "bust" else res2
        return (res1 + res2) / 2

    def _finish_split_ace(self, hand, dealer_hand, strategy):
        if hand_value(hand) == 21:
            return 1
        return self._resolve_final(hand, dealer_hand, strategy)

    def _resolve_final(self, hand, dealer_hand, strategy):
        while hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deck.deal_card())
        if hand_value(hand) > hand_value(dealer_hand) or hand_value(dealer_hand) > 21:
            return 1
        elif hand_value(hand) < hand_value(dealer_hand):
            return -1
        return 0
