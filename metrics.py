import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_psnr(original_path, stego_path):
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)

    mse = np.mean((original.astype("float") - stego.astype("float")) ** 2)

    if mse == 0:
        return 100

    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr


def calculate_ssim(original_path, stego_path):
    original = cv2.imread(original_path)
    stego = cv2.imread(stego_path)

    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    stego_gray = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(original_gray, stego_gray, full=True)
    return score