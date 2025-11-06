import random
from typing import List

class PlayerStrategy:
    def should_hit(self, player_hand: List[str], dealer_upcard: str) -> bool:
        raise NotImplementedError


class RandomStrategy(PlayerStrategy):
    def should_hit(self, player_hand: List[str], dealer_upcard: str) -> bool:
        return random.choice([True, False])
