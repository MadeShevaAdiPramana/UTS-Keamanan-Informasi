def encrypt_vigenere(text, key):
    result = ""
    key = key.upper()
    text = text.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            key_index += 1
        else:
            result += char

    return result


def decrypt_vigenere(cipher, key):
    result = ""
    key = key.upper()
    cipher = cipher.upper()
    key_index = 0

    for char in cipher:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")
            result += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            key_index += 1
        else:
            result += char

    return result