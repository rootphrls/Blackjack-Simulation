from blackjack.hand import hand_value

def test_ace_adjustment():
    assert hand_value(['A', '9']) == 20
    assert hand_value(['A', '9', 'A']) == 21
    assert hand_value(['A', '9', 'A', 'K']) == 21
