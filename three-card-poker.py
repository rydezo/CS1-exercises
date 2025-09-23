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

# tests
assert_equal(hand_to_string([2, 3, 4]), "2 3 4")
assert_equal(hand_to_string([11, 12, 13]), "J Q K")
assert_equal(hand_to_string([10, 7, 14]), "X 7 A")

def sort_hand(hand: list[int]) -> list[int]:
    """
    Sorts the numbers in the user's hand of cards.
    
    Args:
        hand (list[int]): The original hand of cards
    Returns:
        list[int]: The sorted list of cards
    """
    copy = hand
    result = [0] * 3
    result[0] = max(hand)
    copy.remove(max(hand))
    result[2] = min(hand)
    copy.remove(min(hand))
    result[1] = copy[0]
    return result

# tests
assert_equal(sort_hand([2, 4, 3]), [4, 3, 2])
assert_equal(sort_hand([12, 6, 3]), [12, 6, 3])
assert_equal(sort_hand([7, 8, 9]), [9, 8, 7])