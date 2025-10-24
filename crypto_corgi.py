from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

# 1) Define encrypt_text
# 2) Define decrypt_text

# rotate values
def rotate_values(original_values: list[int], rotation_amount: int) -> list[int]:
    """
    Rotates a list of values according to the rotation formula.

    Args:
        original_values (list[int]): The list of integer values corresponding to ASCII characters.
        rotation_amount (int): The amount for each character to be rotated.
    Returns:
        list[int]: A new list of the rotated values that correspond to the original values.
    """
    rotated_values: list[int] = []
    for value in original_values:
        rotated_values.append((value+rotation_amount-32) % 94 + 32)
    return rotated_values

def encrypt_text(message: str, rotation_amount: int) -> str:
    """
    Encrypts inputted text using the Caesar Cipher.

    Args:
        message (str): Text to be encrypted
        rotation_amount(int): The amount for each character to be rotated.
    Returns:
        str: Encrypted text according to the rotation amount
    """
    ords = [ord(char) for char in message]
    rotated = rotate_values(ords, rotation_amount)
    with_tildes: list[int] = []
    for value in rotated:
        with_tildes.append(value)
        if value < 48:
            with_tildes.append(126)
    result = [chr(o) for o in with_tildes]
    return "".join(result)

def decrypt_text(message: str, rotation_amount: int) -> str:
    """
    Decrypts inputted text inversing the Caesar Cipher.

    Args:
        message (str): Text to be decrypted
        rotation_amount(int): The amount for each character to be rotated.
    Returns:
        str: Decrypted text according to the rotation amount
    """
    ords = [ord(char) for char in message]
    no_tildes = [value for value in ords if value != 126]
    rotated = rotate_values(no_tildes, -rotation_amount)
    result = [chr(o) for o in rotated]
    return "".join(result)
    
assert_equal(encrypt_text("hello", 1), "ifmmp")
assert_equal(encrypt_text("", 10), "")
assert_equal(encrypt_text("text!here", -1), "sdws ~gdqd")

assert_equal(decrypt_text("ifmmp", 1), "hello")
assert_equal(decrypt_text("", 5), "")
assert_equal(decrypt_text("sdws ~gdqd", -1), "text!here")

# 3) Define hash_text
def hash_text(message: str, base: int, hash_size: int) -> int:
    """
    Uniquely hashes a text message into an integer value.
    
    Args:
        message(str): The text message to be hashed.
        base(int): The base value for the hashing formula.
        hash_size(int): The size of the hash table.
    Returns:
        int: The hashed integer value of the message.
    """
    hashed_values = []
    for i, c in enumerate(message):
        hashed_values.append((i + base) ** (ord(c)))
    return sum(hashed_values) % hash_size

assert_equal(hash_text("A", 11, 100), 51)
assert_equal(hash_text("AB", 11, 100), 35)
assert_equal(hash_text("ABC", 11, 100), 52)

ROTATION = 4
BASE = 31
HASH_SIZE = 10**9

@dataclass
class State:
    """
    The current state of the Crypto Corgi application.
    
    Attributes:
        message (str): The latest saved encrypted or decrypted text. After
            encrypting, this should be set to the encrypted text. After
            decrypting, this should be set to the decrypted text (but only if
            it was decrypted successfully).
        latest_hash (str): The latest saved hash. After encrypting, this should be
            set to the hash of the original message. After decrypting, this should
            be unchanged.
        status (str): A string message to display to the user, with information
            about the latest encryption and decryption attempt.
    """
    message: str
    latest_hash: str
    status: str


@route
def index(state: State):
    """
    The main page of the Crypto Corgi application.

    Args:
        state (State): The current state of the application.
    Returns:
        Page: The main page of the Crypto Corgi application.
    """
    return Page(
        state,
        content=[Header("Crypto Corgi"),
                 state.status,
                 "Message:", TextBox("given_message", state.message),
                 Button("Encrypt", "encrypt"),
                 "Hash:", TextBox("latest_hash", state.latest_hash),
                 Button("Decrypt", "decrypt")]
    )


@route
def encrypt(state: State, given_message: str):
    """
    Encrypts the given message and updates the state.
    
    Args:
        state (State): The current state of the application.
        given_message (str): The message to be encrypted.
    Returns:
        Page: The updated main page of the Crypto Corgi application.
    """
    state.message = encrypt_text(given_message, ROTATION)
    state.latest_hash = str(hash_text(given_message, BASE, HASH_SIZE))
    state.status = "Message encrypted and hashed!"
    return index(state)


@route
def decrypt(state: State, given_message: str, given_hash: str):
    """
    Decrypts the given message and updates the state.

    Args:
        state (State): The current state of the application.
        given_message (str): The message to be decrypted.
        given_hash (str): The expected hash of the original message.
    Returns:
        Page: The updated main page of the Crypto Corgi application.
    """
    decrypted_text = decrypt_text(given_message, ROTATION)
    if hash_text(decrypted_text, BASE, HASH_SIZE) == int(given_hash):
        state.message = decrypted_text
        state.status = "Message decrypted successfully!"
    else:
        state.status = "Decryption failed: Hash mismatch!"
    return index(state)

assert_equal(
    decrypt(State("", "", ""), "Lipps$~{svph%~", "533815340"),
    Page(
        State("Hello world!", "", "Message decrypted successfully!"),
        [
            Header("Crypto Corgi"),
            "Message decrypted successfully!",
            "Message:",
            TextBox("given_message", "Hello world!"),
            Button("Encrypt", "encrypt"),
            "Hash:",
            TextBox("latest_hash", ""),
            Button("Decrypt", "decrypt"),
        ],
    ),
)


# Initial version of index page
assert_equal(index(State("", "", "Write your message below")),
             Page(State("", "", "Write your message below"), [
                 Header("Crypto Corgi"),
                 "Write your message below",
                 "Message:",
                 TextBox("given_message", ""),
                 Button("Encrypt", "encrypt"),
                 "Hash:", 
                 TextBox("latest_hash", ""),
                 Button("Decrypt", "decrypt"),
             ]))
# Loading index with content
assert_equal(index(State("Test", "1000", "Write your message below")),
             Page(State("Test", "1000", "Write your message below"), [
                 Header("Crypto Corgi"),
                 "Write your message below",
                 "Message:", TextBox("given_message", "Test"),
                 Button("Encrypt", "encrypt"),
                 "Hash:", TextBox("latest_hash", "1000"),
                 Button("Decrypt", "decrypt"),
             ]))
# Encrypt a message
assert_equal(
    encrypt(State("", "", ""), "Hello world!"),
    Page(
        State("Lipps$~{svph%~", "533815340", "Message encrypted and hashed!"),
        [
            Header("Crypto Corgi"),
            "Message encrypted and hashed!",
            "Message:",
            TextBox("given_message", "Lipps$~{svph%~"),
            Button("Encrypt", "encrypt"),
            "Hash:",
            TextBox("latest_hash", "533815340"),
            Button("Decrypt", "decrypt"),
        ],
    ),
)
# Successful decryption
assert_equal(
    decrypt(State("", "", ""), "Lipps$~{svph%~", "533815340"),
    Page(
        State("Hello world!", "", "Message decrypted successfully!"),
        [
            Header("Crypto Corgi"),
            "Message decrypted successfully!",
            "Message:",
            TextBox("given_message", "Hello world!"),
            Button("Encrypt", "encrypt"),
            "Hash:",
            TextBox("latest_hash", ""),
            Button("Decrypt", "decrypt"),
        ],
    ),
)
# Unsuccessful decryption
assert_equal(
    decrypt(State("The original message", "", ""), "Hello world!", "533815340"),
    Page(State("The original message", "", "Decryption failed: Hash mismatch!"), [
        Header("Crypto Corgi"),
        "Decryption failed: Hash mismatch!",
        "Message:",
        TextBox("given_message", "The original message"),
        Button("Encrypt", "encrypt"),
        "Hash:",
        TextBox("latest_hash", ""),
        Button("Decrypt", "decrypt"),
    ]),
)


# Comment out this line to skip running the actual server.
start_server(State("", "", ""))

# 4) Define main
def main():
    """
    Main function to run the encryption/decryption program.
    
    Args:
        None
    Returns:
        None
    """
    action = input("Enter your desired action. (encrypt/decrypt).")
    if action == "encrypt":
        message = input("Enter your plaintext message.")
        encrypted_message = encrypt_text(message, 23)
        hashed_value = hash_text(message, 31, 1000000000)
        print(f"Your encrypted message is {encrypted_message}, and your hashed value is {hashed_value}.")
    elif action == "decrypt":
        message = input("Enter your encrypted message.")
        decrypted_message = decrypt_text(message, 23)
        expected_hash = input("Enter the expected hash.")
        if int(expected_hash) == hash_text(message, 31, 1000000000):
            print(f"Your decrypted message is {decrypted_message}.")
        else:
            print("error: hashes don't match")
    else:
        print("Please enter a valid action.")

main()