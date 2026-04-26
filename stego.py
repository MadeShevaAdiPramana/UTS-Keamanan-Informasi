import cv2
import numpy as np

DELIMITER = "###END###"


def text_to_binary(text):
    return "".join(format(ord(char), "08b") for char in text)


def binary_to_text(binary):
    result = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        if len(byte) == 8:
            result += chr(int(byte, 2))
    return result


def get_edge_map(image):
    # Membersihkan bit LSB supaya edge saat encode dan decode tetap sama
    clean_image = image.copy()
    clean_image = clean_image & 254

    gray = cv2.cvtColor(clean_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    return edges


def embed_message_adaptive(image_path, message, output_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Gambar tidak ditemukan.")

    message = message + DELIMITER
    binary_message = text_to_binary(message)

    edges = get_edge_map(image)
    edge_pixels = np.count_nonzero(edges)

    capacity = edge_pixels * 3

    if len(binary_message) > capacity:
        raise ValueError("Pesan terlalu panjang untuk gambar ini.")

    data_index = 0
    height, width, channels = image.shape

    for y in range(height):
        for x in range(width):
            if edges[y, x] != 0:
                for c in range(3):
                    if data_index < len(binary_message):
                        pixel_value = int(image[y, x, c])
                        image[y, x, c] = (pixel_value & 254) | int(binary_message[data_index])
                        data_index += 1

                    if data_index >= len(binary_message):
                        cv2.imwrite(output_path, image)
                        return True

    cv2.imwrite(output_path, image)
    return True


def extract_message_adaptive(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Gambar tidak ditemukan.")

    edges = get_edge_map(image)
    binary_data = ""

    height, width, channels = image.shape

    for y in range(height):
        for x in range(width):
            if edges[y, x] != 0:
                for c in range(3):
                    binary_data += str(int(image[y, x, c]) & 1)

                    if len(binary_data) % 8 == 0:
                        decoded_text = binary_to_text(binary_data)

                        if DELIMITER in decoded_text:
                            return decoded_text.replace(DELIMITER, "")

    return None