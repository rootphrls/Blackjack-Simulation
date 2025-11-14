# game.py
# Dit is het hart van het spel.
# Hier wordt een hele ronde blackjack gespeeld volgens de Holland Casino regels.

from .cards import Deck
from .hand import hand_value, is_blackjack
from typing import Optional
from .card_count import CardCounter


class BlackjackGame:
    # Initialiseer het spel met een deck (standaard 6 decks)
    def __init__(self, num_decks: int = 6):
        self.deck = Deck(num_decks)

    def play_round(self, player_strategy, counter: Optional[CardCounter] = None):
        # Speel een enkele ronde blackjack met de gegeven spelerstrategie.

        # Deel handen uit. In Holland Casino krijgt de dealer slechts één open kaart.
        player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        dealer_hand = [self.deck.deal_card()]

        # Als er een counter is en het deck is geschud, reset de counter
        if counter and self.deck.reshuffled:
            counter.reset()

        # Update counter met de gedeelde kaarten
        if counter:
            counter.update(player_hand[0])
            counter.update(player_hand[1])
            counter.update(dealer_hand[0])

        # In Holland Casino, speler wordt meteen 3:2 uitbetaald bij een Blackjack.
        if is_blackjack(player_hand):
            return 1.5

        # Speler maakt zijn actie.
        result = self._play_hand(player_hand, dealer_hand, player_strategy, counter)
        if result == "bust":
            return -1

        # Als speler stopt met spelen pakt de dealer zijn volgende kaart.
        card = self.deck.deal_card()
        if counter and self.deck.reshuffled:
            counter.reset()
        if counter:
            counter.update(card)
        dealer_hand.append(card)

        # Dealer blijft kaarten kopen tot 17
        while hand_value(dealer_hand) < 17:
            c = self.deck.deal_card()
            if counter and self.deck.reshuffled:
                counter.reset()
            if counter:
                counter.update(c)
            dealer_hand.append(c)

        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)

        if dealer_total > 21 or player_total > dealer_total:
            return result
        elif player_total < dealer_total:
            return -abs(result)
        else:
            return 0 

    def _play_hand(self, player_hand, dealer_hand, strategy, counter: Optional[CardCounter]):
        # Speelt een ronde Blackjack volgens Holland Casino regels.
        # Actie van speler wordt bepaald volgens gegeven strategie.
        doubled = False

        while True:
            action = strategy.get_action(player_hand, dealer_hand[0])

            if action == "H":
                c = self.deck.deal_card()
                if counter and self.deck.reshuffled:
                    counter.reset()
                if counter:
                    counter.update(c)
                player_hand.append(c)
                if hand_value(player_hand) > 21:
                    return "bust"

            elif action == "S":
                break

            elif action in ("D", "Dp"):
                # In Holland Casino mag je alleen dubbelen bij een hand van 9, 10 of 11 punten.
                total = hand_value(player_hand)
                if total not in (9, 10, 11):
                    if action == "D":
                        c = self.deck.deal_card()
                        if counter and self.deck.reshuffled:
                            counter.reset()
                        if counter:
                            counter.update(c)
                        player_hand.append(c)
                        if hand_value(player_hand) > 21:
                            return "bust"
                        continue
                    else:
                        break
                doubled = True
                c = self.deck.deal_card()
                if counter and self.deck.reshuffled:
                    counter.reset()
                if counter:
                    counter.update(c)
                player_hand.append(c)
                if hand_value(player_hand) > 21:
                    return "bust"
                break

            elif action == "SP":
                return self._handle_split(player_hand, dealer_hand, strategy, counter)

            else:
                break

        return 2 if doubled else 1

    def _handle_split(self, player_hand, dealer_hand, strategy, counter: Optional[CardCounter]):
        if len(player_hand) != 2:
            return 1

        rank0 = player_hand[0]
        rank1 = player_hand[1]
        if self._card_rank(rank0) != self._card_rank(rank1):
            return 1

        # Voor elke split card wordt er een nieuwe hand aangemaakt.
        first = [rank0, self.deck.deal_card()]
        second = [rank1, self.deck.deal_card()]

        if counter and self.deck.reshuffled:
            counter.reset()
        if counter:
            counter.update(first[1])
            counter.update(second[1])

        if self._card_rank(rank0) == 'A':
            r1 = self._resolve_after_split_ace(first, dealer_hand, counter)
            r2 = self._resolve_after_split_ace(second, dealer_hand, counter)
            return (r1 + r2) / 2

        res1 = self._play_hand(first, dealer_hand, strategy, counter)
        res2 = self._play_hand(second, dealer_hand, strategy, counter)

        res1 = -1 if res1 == "bust" else res1
        res2 = -1 if res2 == "bust" else res2
        return (res1 + res2) / 2

    def _resolve_after_split_ace(self, hand, dealer_hand, counter: Optional[CardCounter]):
        from copy import deepcopy
        dealer_copy = deepcopy(dealer_hand)

        if len(dealer_copy) == 1:
            c = self.deck.deal_card()
            if counter and self.deck.reshuffled:
                counter.reset()
            if counter:
                counter.update(c)
            dealer_copy.append(c)
        while hand_value(dealer_copy) < 17:
            c = self.deck.deal_card()
            if counter and self.deck.reshuffled:
                counter.reset()
            if counter:
                counter.update(c)
            dealer_copy.append(c)
            
        if hand_value(hand) > 21:
            return -1
        if hand_value(dealer_copy) > 21 or hand_value(hand) > hand_value(dealer_copy):
            return 1
        if hand_value(hand) < hand_value(dealer_copy):
            return -1
        return 0

    def _card_rank(self, card: str) -> str:
        return {'J': '10', 'Q': '10', 'K': '10'}.get(card, card)
