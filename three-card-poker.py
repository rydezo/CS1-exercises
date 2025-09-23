from bakery import assert_equal

def hand_to_string(hand: list[int]) -> str:
    """
    Convert the player's hand of cards from a list of integers to
    a string suitable for showing the hand to the player.
    
    Args:
        hand (list[int]): A list of integers representing the player's hand.
    Returns:
        str: The player's hand in a readable, single-line format
    """
    face_cards = {
        10: "X",
        11: "J",
        12: "Q",
        13: "K",
        14: "A"
    }
    result = []
    for card in hand:
        if 2 <= card <= 9:
            result.append(str(card))
        else:
            result.append(face_cards[card])
    return " ".join(result)

assert_equal(hand_to_string([2, 3, 4]), "2 3 4")
assert_equal(hand_to_string([11, 12, 13]), "J Q K")
assert_equal(hand_to_string([10, 7, 14]), "X 7 A")