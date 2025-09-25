from bakery import assert_equal
from string import ascii_lowercase
from drafter import *
from random import choice
from dataclasses import dataclass


LEVELS = ["heat", "dogs", "jazz"]


def choose_word(level: int) -> str:
    """
    Choose a word from the LEVELS list based on the given level.
    Must be a valid level index (starting from 0).

    Args:
        level (int): The level of the word to choose.
    Returns:
        str: The chosen word.
    """
    return LEVELS[level]


assert_equal(choose_word(0), "heat")
assert_equal(choose_word(1), "dogs")
assert_equal(choose_word(2), "jazz")


def reveal_letter(secret: str, guesses: list[str], index: int) -> str:
    """
    Reveal a letter in the secret word if it has been guessed.
    The index must be a valid position in the word.

    Args:
        secret (str): The secret word.
        guesses (list[str]): The list of guessed letters.
        index (int): The index of the letter to reveal.

    Returns:
        str: The revealed letter or "_" if not guessed.
    """
    if secret[index] in guesses:
        return secret[index]
    return "_"


assert_equal(reveal_letter("heat", ["h"], 0), "h")
assert_equal(reveal_letter("heat", ["h"], 1), "_")
assert_equal(reveal_letter("heat", ["h"], 2), "_")
assert_equal(reveal_letter("heat", ["h"], 3), "_")
assert_equal(reveal_letter("heat", ["x"], 0), "_")
assert_equal(reveal_letter("heat", ["t"], 3), "t")
assert_equal(reveal_letter("heat", ["r", "x", "q"], 0), "_")
assert_equal(reveal_letter("heat", ["r", "x", "h"], 0), "h")
assert_equal(reveal_letter("heat", ["r", "x", "h"], 1), "_")


def reveal(secret: str, guesses: list[str]) -> str:
    """
    Reveal the letters in the secret word that have been guessed.

    Args:
        secret (str): The secret word.
        guesses (list[str]): The list of guessed letters.

    Returns:
        str: The revealed letters or "_" for unguessed letters.
    """
    c0 = reveal_letter(secret, guesses, 0)
    c1 = reveal_letter(secret, guesses, 1)
    c2 = reveal_letter(secret, guesses, 2)
    c3 = reveal_letter(secret, guesses, 3)
    return c0 + c1 + c2 + c3


assert_equal(reveal("heat", ["h"]), "h___")
assert_equal(reveal("heat", ["a"]), "__a_")
assert_equal(reveal("heat", ["t"]), "___t")
assert_equal(reveal("heat", ["e", "a"]), "_ea_")
assert_equal(reveal("heat", ["x"]), "____")
assert_equal(reveal("heat", ["h", "e", "a", "t"]), "heat")
assert_equal(reveal("heat", ["h", "e", "a", "r"]), "hea_")


def is_win(secret: str, guesses: list[str]) -> bool:
    """
    Check if the player has won the game by guessing all letters in the secret word.

    Args:
        secret (str): The secret word.
        guesses (list[str]): The list of guessed letters.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    if secret[0] not in guesses:
        return False
    if secret[1] not in guesses:
        return False
    if secret[2] not in guesses:
        return False
    if secret[3] not in guesses:
        return False
    return True


assert_equal(is_win("heat", ["h"]), False)
assert_equal(is_win("heat", ["h", "e"]), False)
assert_equal(is_win("heat", ["h", "e", "a"]), False)
assert_equal(is_win("heat", ["h", "e", "a", "t"]), True)
assert_equal(is_win("heat", ["t", "e", "a", "h"]), True)
assert_equal(is_win("heat", ["t", "e", "a", "r", "h"]), True)


def is_loss(wrong: int) -> bool:
    """
    Check if the player has lost the game by making too many incorrect guesses.

    Args:
        wrong (int): The number of incorrect guesses made by the player.

    Returns:
        bool: Whether the player has guessed too many times.
    """
    return wrong >= 6


assert_equal(is_loss(0), False)
assert_equal(is_loss(5), False)
assert_equal(is_loss(6), True)
assert_equal(is_loss(7), True)


def in_secret(secret: str, character: str) -> bool:
    """
    Check if a character is in the secret word.

    Args:
        secret (str): The secret word.
        character (str): The character to check.

    Returns:
        bool: True if the character is in the secret word, False otherwise.
    """
    return character in secret


assert_equal(in_secret("heat", "h"), True)
assert_equal(in_secret("heat", "a"), True)
assert_equal(in_secret("heat", "t"), True)
assert_equal(in_secret("heat", "e"), True)
assert_equal(in_secret("heat", "x"), False)


def format_guess(guess: str) -> str:
    """
    Format the player's guess by stripping whitespace and converting to lowercase.

    Args:
        guess (str): The player's guess.

    Returns:
        str: The formatted guess.
    """
    return guess.lower().strip()


assert_equal(format_guess(" H "), "h")
assert_equal(format_guess("      A "), "a")
assert_equal(format_guess("t"), "t")


def check_if_valid_guess(guess: str, guesses: list[str]) -> bool:
    """
    Check if the player's guess is valid.

    Args:
        guess (str): The player's guess.
        guesses (list[str]): The list of previously guessed letters.

    Returns:
        bool: True if the guess is valid, False otherwise.
    """
    return len(guess) == 1 and guess in ascii_lowercase and guess not in guesses


assert_equal(check_if_valid_guess("h", []), True)
assert_equal(check_if_valid_guess("H", []), False)
assert_equal(check_if_valid_guess("1", []), False)
assert_equal(check_if_valid_guess("", []), False)
assert_equal(check_if_valid_guess("hello", []), False)
assert_equal(check_if_valid_guess("oH", []), False)
assert_equal(check_if_valid_guess("!", []), False)
assert_equal(check_if_valid_guess("h", ["h"]), False)
assert_equal(check_if_valid_guess("h", ["x", "y", "h"]), False)
assert_equal(check_if_valid_guess("z", ["x", "y", "h"]), True)


def is_game_over(level: int) -> bool:
    """
    Check if the game is over.

    Args:
        level (int): The current level of the game.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    return level > len(LEVELS) - 1


assert_equal(is_game_over(0), False)
assert_equal(is_game_over(2), False)
assert_equal(is_game_over(3), True)


#### Drafter UI


@dataclass
class State:
    """
    Represents the state of the game.

    Attributes:
        secret (str): The secret word to guess.
        guesses (list[str]): The list of guessed letters.
        wrong (int): The number of incorrect guesses made by the player.
        level (int): The current level of the game.
        score (int): The player's score.
    """

    secret: str
    guesses: list[str]
    wrong: int
    level: int
    score: int


@route
def index(state: State) -> Page:
    """
    Render the title screen, with a button to start the game.

    Args:
        state (State): The current state of the game.

    Returns:
        Page: The rendered index page.
    """
    return Page(
        state,
        [
            Header("Guess the Word"),
            "Level: " + str(state.level),
            Button("Start", "next_level"),
        ],
    )


assert_equal(
    index(State("heat", [], 0, 0, 0)),
    Page(
        State("heat", [], 0, 0, 0),
        [
            Header("Guess the Word"),
            "Level: 0",
            Button("Start", "next_level"),
        ],
    ),
)


@route
def next_level(state: State) -> Page:
    """
    Move to the next level of the game, increasing the level,
    choosing a new word, and resetting the guesses.
    If the game is over, then transition to the game over page.
    Otherwise, render the play level page.

    Args:
        state (State): The current state of the game.

    Returns:
        Page: The rendered page for the next level.
    """
    state.level += 1
    state.secret = choose_word(state.level)
    state.guesses = []
    state.wrong = 0
    if is_game_over(state.level):
        return game_end(state)
    return play_level(state)


@route
def play_level(state: State) -> Page:
    """
    Render the play level page, including the current revealed
    word, the list of guessed letters, and the number of wrong guesses.
    Provide a text box for the player to enter their guess.

    Args:
        state (State): The current state of the game.

    Returns:
        Page: The rendered play level page.
    """
    so_far = reveal(state.secret, state.guesses)
    return Page(
        state,
        [
            Header("Level " + str(state.level)),
            "Word: " + so_far,
            "Guesses so far: ",
            BulletedList(state.guesses),
            "Guess a letter:",
            TextBox("guess"),
            Button("Submit", "submit_guess"),
        ],
    )


@route
def submit_guess(state: State, guess: str) -> Page:
    """
    Handle the submission of a player's guess.
    If the guess is valid, remember the guess and check if
    the player has won the level.
    If they have won, show the win screen; if they have lost,
    show the lose screen.
    Otherwise, keep playing.

    Args:
        state (State): The current state of the game.
        guess (str): The player's single letter guess.

    Returns:
        Page: The rendered page after submitting the guess.
    """
    guess = format_guess(guess)
    if not check_if_valid_guess(guess, state.guesses):
        return play_level(state)

    state.guesses.append(guess)
    if not in_secret(state.secret, guess):
        state.wrong += 1

    if is_win(state.secret, state.guesses):
        return win_level(state)

    if is_loss(state.wrong):
        return lose_level(state)

    return play_level(state)


assert_equal(
    submit_guess(State("heat", [], 0, 0, 0), "h"),
    Page(
        State("heat", ["h"], 0, 0, 0),
        [
            Header("Level 0"),
            "Word: h___",
            "Guesses so far: ",
            BulletedList(["h"]),
            "Guess a letter:",
            TextBox("guess"),
            Button("Submit", "submit_guess"),
        ],
    ),
)


@route
def win_level(state: State) -> Page:
    """
    Render the win level page, including the current score and a button to continue.

    Args:
        state (State): The current state of the game.

    Returns:
        Page: The rendered win level page.
    """
    state.score += 1
    return Page(
        state,
        [
            Header("You Win!"),
            "The word was: " + state.secret,
            Button("Play Again", "next_level"),
        ],
    )


@route
def lose_level(state: State) -> Page:
    """
    Render the lose level page, including the current score and a button to continue.

    Args:
        state (State): The current state of the game.

    Returns:
        Page: The rendered lose level page.
    """
    return Page(
        state,
        [
            Header("You Lost!"),
            "The word was: " + state.secret,
            Button("Play Again", "next_level"),
        ],
    )


@route
def game_end(state: State) -> Page:
    """
    Render the game over page, including the final score.
    """
    return Page(
        state,
        [
            Header("Game Over"),
            "The word was: " + state.secret,
            "Your final score is: " + str(state.score),
        ],
    )


#### Integration Tests

initial_state = State("", [], 0, -1, 0)

after_index = index(initial_state).state
assert_equal(after_index, State("", [], 0, -1, 0))

level_1 = next_level(after_index).state
assert_equal(level_1, State("heat", [], 0, 0, 0))

first_guess = submit_guess(level_1, "x").state
assert_equal(first_guess, State("heat", ["x"], 1, 0, 0))

close_to_heat = State("heat", ["h", "e", "a"], 0, 0, 0)

won_level = submit_guess(close_to_heat, "t").state
assert_equal(won_level, State("heat", ["h", "e", "a", "t"], 0, 0, 1))

level_2 = next_level(won_level).state
assert_equal(level_2, State("dogs", [], 0, 1, 1))

#### Start Game

start_server(State("", [], 0, -1, 0))