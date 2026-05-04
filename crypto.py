# fungsi untuk enkripsi menggunakan Vigenere Cipher
def encrypt_vigenere(text, key):
    result = ""  # menyimpan hasil ciphertext

    # ubah key dan text ke huruf besar agar konsisten (A-Z)
    key = key.upper()
    text = text.upper()

    key_index = 0  # index untuk perulangan key

    # loop setiap karakter dalam text
    for char in text:
        # cek apakah karakter adalah huruf
        if char.isalpha():

            # ambil nilai pergeseran dari key (A=0, B=1, ..., Z=25)
            shift = ord(key[key_index % len(key)]) - ord("A")

            # proses enkripsi:
            # ubah huruf ke angka → tambah shift → mod 26 → balik ke huruf
            result += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))

            # pindah ke huruf key berikutnya
            key_index += 1
        else:
            # jika bukan huruf (spasi, angka, simbol) → tidak diubah
            result += char

    return result  # kembalikan hasil ciphertext


# fungsi untuk dekripsi menggunakan Vigenere Cipher
def decrypt_vigenere(cipher, key):
    result = ""  # menyimpan hasil plaintext

    # ubah ke huruf besar
    key = key.upper()
    cipher = cipher.upper()

    key_index = 0  # index untuk key

    # loop setiap karakter ciphertext
    for char in cipher:
        # cek apakah huruf
        if char.isalpha():

            # ambil nilai pergeseran dari key
            shift = ord(key[key_index % len(key)]) - ord("A")

            # proses dekripsi:
            # ubah huruf ke angka → kurangi shift → mod 26 → balik ke huruf
            result += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))

            # pindah ke huruf key berikutnya
            key_index += 1
        else:
            # karakter selain huruf tidak diubah
            result += char

    return result  # kembalikan plaintext