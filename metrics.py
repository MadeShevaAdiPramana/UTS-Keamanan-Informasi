import cv2  # library untuk pengolahan gambar
import numpy as np  # library untuk operasi numerik (array, matrix)
from skimage.metrics import structural_similarity as ssim  # fungsi SSIM


# fungsi untuk menghitung PSNR (Peak Signal-to-Noise Ratio)
def calculate_psnr(original_path, stego_path):

    # membaca gambar asli dan gambar hasil steganografi
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)

    # menghitung MSE (Mean Squared Error)
    # selisih setiap pixel → dikuadratkan → dirata-ratakan
    mse = np.mean((original.astype("float") - stego.astype("float")) ** 2)

    # jika tidak ada perbedaan sama sekali (gambar identik)
    if mse == 0:
        return 100  # nilai PSNR maksimum

    # rumus PSNR:
    # PSNR = 20 * log10(MAX / sqrt(MSE))
    # MAX = 255 (nilai maksimum pixel)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))

    return psnr  # mengembalikan nilai PSNR


# fungsi untuk menghitung SSIM (Structural Similarity Index)
def calculate_ssim(original_path, stego_path):

    # membaca gambar asli dan stego
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)

    # mengubah gambar menjadi grayscale (abu-abu)
    # karena SSIM biasanya dihitung pada citra grayscale
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)

    # menghitung SSIM
    # score = nilai kemiripan (0 sampai 1)
    # semakin mendekati 1 → semakin mirip
    score, _ = ssim(original_gray, stego_gray, full=True)

    return score  # mengembalikan nilai SSIM