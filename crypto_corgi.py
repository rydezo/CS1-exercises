from bakery import assert_equal

# 1) Define encrypt_text
# 2) Define decrypt_text

# rotate values
def rotate_values(original_values: list[int], rotation_amount: int) -> list[int]:
    """
    Rotates a list of values according to the rotation formula.

    Args:
        original_values(list[int]): The list of integer values corresponding to ASCII characters.
        rotation_amount(int): The amount for each character to be rotated.
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
        message: Text to be encrypted
        rotation_amount(int): The amount for each character to be rotated.
    Returns:
        str: Encrypted text according to the rotation amount
    """
    ASCII_strings: list[int] = []
    for char in message:
        ASCII_strings.append(ord(char))
    rotated = rotate_values(ASCII_strings, rotation_amount)
    updated: list[int] = []
    for value in rotated:
        updated.append(value)
        if value < 48:
            updated.append(126)
    result: list[int] = []
    for num in updated:
        result.append(chr(num))
    return "".join(result)

def decrypt_text(message: str, rotation_amount: int) -> str:
    """
    Decrypts inputted text inversing the Caesar Cipher.

    Args:
        message: Text to be decrypted
        rotation_amount(int): The amount for each character to be rotated.
    Returns:
        str: Decrypted text according to the rotation amount
    """
    ASCII_strings: list[int] = []
    for char in message:
        ASCII_strings.append(ord(char))
    no_tildes: list[str] = []
    for value in ASCII_strings:
        if value != 126:
            no_tildes.append(value)
    rotated = rotate_values(no_tildes, -rotation_amount)
    result: list[int] = []
    for num in rotated:
        result.append(chr(num))
    return "".join(result)
    
assert_equal(encrypt_text("hello", 1), "ifmmp")
assert_equal(encrypt_text("text!here", -1), "sdws ~gdqd")

assert_equal(decrypt_text("ifmmp", 1), "hello")
assert_equal(decrypt_text("sdws ~gdqd", -1), "text!here")