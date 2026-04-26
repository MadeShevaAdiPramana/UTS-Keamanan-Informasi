from crypto import encrypt_vigenere, decrypt_vigenere
from stego import embed_message_adaptive, extract_message_adaptive
from metrics import calculate_psnr, calculate_ssim

message = "HALO INI PESAN RAHASIA"
key = "KUNCI"

cover_image = "input.png"
stego_image = "output.png"

ciphertext = encrypt_vigenere(message, key)
print("Ciphertext:", ciphertext)

embed_message_adaptive(cover_image, ciphertext, stego_image)
print("Pesan berhasil disisipkan.")

psnr = calculate_psnr(cover_image, stego_image)
ssim = calculate_ssim(cover_image, stego_image)

print("PSNR:", psnr)
print("SSIM:", ssim)

extracted_ciphertext = extract_message_adaptive(stego_image)
plaintext = decrypt_vigenere(extracted_ciphertext, key)

print("Pesan hasil decode:", plaintext)