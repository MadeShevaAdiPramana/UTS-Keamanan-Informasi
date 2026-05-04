# import fungsi enkripsi dan dekripsi Vigenere Cipher
from crypto import encrypt_vigenere, decrypt_vigenere

# import fungsi steganografi untuk embed dan extract pesan
from stego import embed_message_adaptive, extract_message_adaptive

# import fungsi evaluasi kualitas gambar
from metrics import calculate_psnr, calculate_ssim


# pesan asli yang akan diamankan
message = "HALO INI PESAN RAHASIA"

# kunci untuk proses enkripsi dan dekripsi Vigenere
key = "KUNCI"

# gambar asli sebagai media penyisipan pesan
cover_image = "input.png"

# gambar hasil steganografi
stego_image = "output.png"


# proses enkripsi pesan menggunakan Vigenere Cipher
ciphertext = encrypt_vigenere(message, key)

# menampilkan hasil enkripsi
print("Ciphertext:", ciphertext)


# menyisipkan ciphertext ke dalam gambar menggunakan Adaptive Edge-Based LSB
embed_message_adaptive(cover_image, ciphertext, stego_image)

# menampilkan status bahwa pesan berhasil disisipkan
print("Pesan berhasil disisipkan.")


# menghitung kualitas gambar hasil steganografi menggunakan PSNR
psnr = calculate_psnr(cover_image, stego_image)

# menghitung kemiripan struktur gambar menggunakan SSIM
ssim = calculate_ssim(cover_image, stego_image)


# menampilkan nilai PSNR
print("PSNR:", psnr)

# menampilkan nilai SSIM
print("SSIM:", ssim)


# mengambil kembali ciphertext dari gambar stego
extracted_ciphertext = extract_message_adaptive(stego_image)

# mendekripsi ciphertext menjadi pesan asli
plaintext = decrypt_vigenere(extracted_ciphertext, key)


# menampilkan pesan hasil decode
print("Pesan hasil decode:", plaintext)