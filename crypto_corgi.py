from bakery import assert_equal

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
    updated: list[int] = []
    for value in rotated:
        updated.append(value)
        if value < 48:
            updated.append(126)
    result = [chr(o) for o in updated]
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

from bakery import assert_equal

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