from bakery import assert_equal

# 1) Define encrypt_text
# 2) Define decrypt_text

# rotate values
def rotate_values(original_values: list[int], rotation_amount: int) -> list[int]:
    rotated_values: list[int] = []
    for value in original_values:
        rotated_values.append((value+rotation_amount-32) % 94 + 32)
    return rotated_values

def encrypt_text(message: str, rotation_amount: int) -> str:
    ASCII_strings: list[int] = []
    for char in message:
        ASCII_strings.append(ord(char))
    rotated = rotate_values(ASCII_strings, rotation_amount)
    for i in range(len(rotated)-1, 0, -1):
        if rotated[i] < 48:
            rotated.insert(i+1, 126)
    result: list[int] = []
    for num in rotated:
        result.append(chr(num))
    return "".join(result)

def decrypt_text(message: str, rotation_amount: int) -> str:
    ASCII_strings: list[int] = []
    for char in message:
        ASCII_strings.append(ord(char))
    no_tildes: list[str] = []
    for value in ASCII_strings:
        if value != 126:
            no_tildes.append(value)
    rotated = rotate_values(no_tildes, rotation_amount)
    result: list[int] = []
    for num in rotated:
        result.append(chr(num))
    return "".join(result)
    
assert_equal(encrypt_text("hello", 1), "ifmmp")