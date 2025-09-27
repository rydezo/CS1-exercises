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

def has_triple(hand: list[int]) -> bool:
    """
    Determines if the hand has three identical numbers.
    
    Args:
        hand (list[int]): The hand of cards
    Returns:
        bool: Whether the hand has three identical numbers
    """
    return hand[0] == hand[1] == hand[2]

assert_equal(has_triple([2, 3, 4]), False)
assert_equal(has_triple([3, 3, 3]), True)
assert_equal(has_triple([7, 7, 7]), True)

def has_straight(hand: list[int]) -> bool:
    '''
    Determines if the hand has three numbers in direct, 
    consecutive order from largest to smallest
    
    Args:
        hand (list[int]): The hand of cards sorted from largest to smallest
    Returns:
        bool: Whether the hand of cards is in direct, 
        consecutive order from largest to smallest
    '''
    return hand[0] == hand[1] + 1 == hand[2] + 2

assert_equal(has_straight([4, 3, 2]), True)
assert_equal(has_straight([2, 3, 4]), False)
assert_equal(has_straight([5, 3, 2]), False)

def has_pair(hand: list[int]) -> bool:
    '''
    Determines if the hand has two identical numbers (a "pair")
    
    Args:
        hand (list[int]): The hand of sorted cards
    Returns:
        bool: Whether the hand has a pair
    '''
    return len(set(hand)) < 3

assert_equal(has_pair([4, 3, 2]), False)
assert_equal(has_pair([5, 3, 3]), True)
assert_equal(has_pair([7, 7, 10]), True)

def score_hand(hand: list[int]) -> int:
    '''
    Scores a sorted hand of cards according to scoring guidelines.
    
    Args:
        hand (list[int]): Sorted hand of cards
    Returns:
        int: Numerical score of the hand of cards
    '''
    score = 0
    # score feature functions
    if has_triple(hand):
        score += 16 ** 4
    elif has_straight(hand):
        score += 15 * (16 ** 3)
    elif has_pair(hand):
        repeated_num = hand[0] if hand[0] == hand[1] else hand[2]
        score += repeated_num * (16 ** 3)
    
    for i in range(3):
        score += hand[i] * (16 ** (2-i))
    
    return score

assert_equal(score_hand([7, 4, 4]), 18244)
assert_equal(score_hand([3, 3, 2]), 13106)
assert_equal(score_hand([11, 10, 9]), 64425)
assert_equal(score_hand([3, 3, 3]), 66355)
assert_equal(score_hand([5, 3, 2]), 1330)

def dealer_plays(hand: list[int]) -> bool:
    '''
    Determines whether the hand has a queen high or better
    
    Args:
        hand (list[int]): Hand of cards
    Returns:
        bool: Whether the hand has a queen high or better
    '''
    return has_pair(hand) or has_triple(hand) or has_straight(hand) or hand[0] >= 12

assert_equal(dealer_plays([4, 3, 2]), True)
assert_equal(dealer_plays([12, 7, 2]), True)
assert_equal(dealer_plays([9, 8, 6]), False)

def play_round() -> int:
    '''
    Plays a single round of three-card poker.
    
    Returns:
        int: The score change from the round
    '''
    player_cards = sort_hand(deal())
    print("Your hand is:", hand_to_string(player_cards))
    player_score = score_hand(player_cards)
    player_choice = get_choice()
    if player_choice == "f":
        return -10
    else:
        dealer_cards = sort_hand(deal())
        print("Dealer's hand is:", hand_to_string(dealer_cards))
        dealer_score = score_hand(dealer_cards)
        if not dealer_plays(dealer_cards):
            return 10
        else:
            return 20 if player_score >= dealer_score else -20

def get_choice() -> str:
    """
    Get user input and return either 'p' or 'f' depending on the player's choice.
    """
    answer= ' '
    while answer not in 'pf':
        answer=input("Please enter either 'p' or 'f':")
    return answer

from random import randint

def deal() -> list[int]:
    """
    Simple random card dealing function that returns three randomly chosen cards,
    represented as integers between 2 and 14.
    """
    return [randint(2, 14), randint(2, 14), randint(2, 14)]

score = 0
while True:
    score += play_round()
    print("Your score is", score, "- Starting a new round!")

    play_again = input("Do you want to keep playing? (y/n): ").lower()
    if play_again != "y":
        break

from drafter import *
from dataclasses import dataclass

@dataclass
class State:
    hand: list[int]
    dealer_hand: list[int]
    score: int


def decide_game(state: State) -> str:
    if not dealer_plays(state.dealer_hand):
        state.score += 10
        dealer_action = "folded"
    elif score_hand(sort_hand(state.dealer_hand)) < score_hand(sort_hand(state.hand)):
        state.score += 20
        dealer_action = "won"
    else:
        state.score -= 20
        dealer_action = "lost"
    return dealer_action

@route
def index(state: State):
    state.hand = deal()
    state.dealer_hand = deal()
    return Page(
        state,
        [
            Header("New round!"),
            "Your score: " + str(state.score),
            "Your hand: " + hand_to_string(state.hand),
            Button("Fold", fold),
            Button("Play", play),
        ],
    )


@route
def fold(state: State):
    state.score -= 10
    return Page(
        state,
        [
            Header("You folded!"),
            "You lost 10 points. Your score is now " + str(state.score),
            Button("Start new game", index),
        ],
    )


@route
def play(state: State):
    dealer_action = decide_game(state)
    return Page(
        state,
        [
            Header("Dealer " + dealer_action + "!"),
            "Your hand: " + hand_to_string(state.hand),
            "The dealer's hand: " + hand_to_string(state.dealer_hand),
            "The dealer " + dealer_action + " and your score is now " + str(state.score) + " points.",
            Button("Start new game", index),
        ],
    )


start_server(State([], [], 0))