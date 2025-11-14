# strategy.py
# Dit bestand bevat implementaties van verschillende blackjack-strategieën.
# We gebruiken hier een bepaalde soort van basisstrategie aangepast voor Holland Casino en een willekeurige strategie (random strategy).

import random
from typing import List
from .hand import hand_value


class PlayerStrategy:
    # Dit is een abstracte basisstrategie klasse.
    # In programmeertermen betekent dit dat we een interface definiëren die andere strategieën moeten implementeren.
    def get_action(self, player_hand: List[str], dealer_upcard: str) -> str:
        raise NotImplementedError

    def should_hit(self, player_hand: List[str], dealer_upcard: str) -> bool:
        action = self.get_action(player_hand, dealer_upcard)
        return action in ("H", "D")


class BasicStrategy(PlayerStrategy):
    # Elke tabel definieert de acties voor verschillende situaties.
    # "H" = Hit, "S" = Stand, "D" = Double Down, "SP" = Split
    # Tabellen zijn gebaseerd op standaard blackjack basisstrategie aangepast voor Holland Casino regels.
    # Voor deze tabel maken we gebruik van Meneer Casino (https://meneercasino.com/online-casino-tips/blackjack-holland-casino-strategie).
    hard_totals = {
        5: {i: "H" for i in range(2, 12)},
        6: {i: "H" for i in range(2, 12)},
        7: {i: "H" for i in range(2, 12)},
        8: {i: "H" for i in range(2, 12)},
        9: {2: "H", 3: "D", 4: "D", 5: "D", 6: "D", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        10: {2: "D", 3: "D", 4: "D", 5: "D", 6: "D", 7: "D", 8: "D", 9: "D", 10: "H", 11: "H"},
        11: {2: "D", 3: "D", 4: "D", 5: "D", 6: "D", 7: "D", 8: "D", 9: "D", 10: "H", 11: "H"},
        12: {2: "H", 3: "H", 4: "S", 5: "S", 6: "S", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        13: {2: "S", 3: "S", 4: "S", 5: "S", 6: "S", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        14: {2: "S", 3: "S", 4: "S", 5: "S", 6: "S", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        15: {2: "S", 3: "S", 4: "S", 5: "S", 6: "S", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        16: {2: "S", 3: "S", 4: "S", 5: "S", 6: "S", 7: "H", 8: "H", 9: "H", 10: "H", 11: "H"},
        17: {i: "S" for i in range(2, 12)},
        18: {i: "S" for i in range(2, 12)},
        19: {i: "S" for i in range(2, 12)},
        20: {i: "S" for i in range(2, 12)},
        21: {i: "S" for i in range(2, 12)},
    }
    soft_totals = {
        13: {i: "H" for i in range(2, 12)},
        14: {i: "H" for i in range(2, 12)},
        15: {i: "H" for i in range(2, 12)},
        16: {i: "H" for i in range(2, 12)},  
        17: {i: "H" for i in range(2, 12)},  
        18: {2: "S", 3: "S", 4: "S", 5: "S", 6: "S", 7: "S", 8: "S", 9: "H", 10: "H", 11: "H"},
        19: {i: "S" for i in range(2, 12)},
        20: {i: "S" for i in range(2, 12)},
        21: {i: "S" for i in range(2, 12)},
    }
    pair_totals = {
        '2': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
        '3': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
        '4': {2:"H",3:"H",4:"H",5:"SP",6:"SP",7:"H",8:"H",9:"H",10:"H",11:"H"},
        '5': {2:"D",3:"D",4:"D",5:"D",6:"D",7:"D",8:"D",9:"D",10:"H",11:"H"},
        '6': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"H",8:"H",9:"H",10:"H",11:"H"},
        '7': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"H",9:"H",10:"H",11:"H"},
        '8': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"SP",9:"SP",10:"H",11:"H"},
        '9': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"S",8:"SP",9:"SP",10:"S",11:"S"},
        '10': {i:"S" for i in range(2,12)},
        'A': {2:"SP",3:"SP",4:"SP",5:"SP",6:"SP",7:"SP",8:"SP",9:"SP",10:"H",11:"H"},
    }

    def get_action(self, player_hand: List[str], dealer_upcard: str) -> str:
        total = hand_value(player_hand)
        dealer_val = self._dealer_value(dealer_upcard)
        is_soft = self._is_soft(player_hand)
        is_pair = self._is_pair(player_hand)

        if is_pair:
            return self._pair_decision(player_hand[0], dealer_val)
        elif is_soft:
            return self._soft_decision(total, dealer_val)
        else:
            return self._hard_decision(total, dealer_val)

    def _dealer_value(self, card: str) -> int:
        if card in ['J', 'Q', 'K']:
            return 10
        elif card == 'A':
            return 11
        return int(card)

    def _is_soft(self, hand: List[str]) -> bool:
        aces = hand.count('A')
        if aces == 0:
            return False
        total = sum(11 if c == 'A' else 10 if c in 'JQK' else int(c) for c in hand)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return aces > 0

    def _is_pair(self, hand: List[str]) -> bool:
        return len(hand) == 2 and self._card_rank(hand[0]) == self._card_rank(hand[1])

    def _card_rank(self, card: str) -> str:
        return {'J': '10', 'Q': '10', 'K': '10'}.get(card, card)

    def _hard_decision(self, total: int, dealer: int) -> str:
        dealer = 11 if dealer == 1 else dealer
        return self.hard_totals.get(total, {}).get(dealer, "H")

    def _soft_decision(self, total: int, dealer: int) -> str:
        dealer = 11 if dealer == 1 else dealer
        return self.soft_totals.get(total, {}).get(dealer, "H")

    def _pair_decision(self, rank: str, dealer: int) -> str:
        dealer = 11 if dealer == 1 else dealer
        rank = self._card_rank(rank)
        return self.pair_totals.get(rank, {}).get(dealer, "H")


class RandomStrategy(PlayerStrategy):
    def get_action(self, player_hand: List[str], dealer_upcard: str) -> str:
        return random.choice(["H", "S", "D"])
