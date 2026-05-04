import cv2  # library OpenCV untuk membaca, menulis, dan memproses gambar
import numpy as np  # library untuk operasi array/matriks pada gambar

# penanda akhir pesan, agar saat ekstraksi program tahu pesan sudah selesai
DELIMITER = "###END###"


# mengubah teks menjadi deretan biner 8-bit
def text_to_binary(text):
    # setiap karakter diubah ke kode ASCII, lalu diformat menjadi 8 bit
    return "".join(format(ord(char), "08b") for char in text)


# mengubah deretan biner kembali menjadi teks
def binary_to_text(binary):
    result = ""

    # membaca data biner per 8 bit = 1 karakter
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]

        # hanya proses jika panjang byte lengkap 8 bit
        if len(byte) == 8:
            result += chr(int(byte, 2))

    return result


# membuat peta tepi gambar menggunakan metode Canny Edge Detection
def get_edge_map(image):
    # membersihkan bit LSB agar hasil edge detection saat encode dan decode tetap konsisten
    clean_image = image.copy()
    clean_image = clean_image & 254  # mengubah bit terakhir menjadi 0

    # mengubah gambar dari BGR ke grayscale
    gray = cv2.cvtColor(clean_image, cv2.COLOR_BGR2GRAY)

    # mendeteksi area tepi menggunakan Canny
    edges = cv2.Canny(gray, 100, 200)

    return edges


# fungsi untuk menyisipkan pesan ke dalam gambar
def embed_message_adaptive(image_path, message, output_path):
    # membaca gambar dari path
    image = cv2.imread(image_path)

    # validasi jika gambar gagal dibaca
    if image is None:
        raise ValueError("Gambar tidak ditemukan.")

    # menambahkan delimiter sebagai tanda akhir pesan
    message = message + DELIMITER

    # mengubah pesan menjadi biner
    binary_message = text_to_binary(message)

    # mendapatkan area tepi gambar
    edges = get_edge_map(image)

    # menghitung jumlah pixel yang termasuk edge
    edge_pixels = np.count_nonzero(edges)

    # kapasitas = jumlah pixel edge x 3 channel warna RGB/BGR
    # setiap channel menyimpan 1 bit pesan
    capacity = edge_pixels * 3

    # validasi apakah kapasitas gambar cukup
    if len(binary_message) > capacity:
        raise ValueError("Pesan terlalu panjang untuk gambar ini.")

    data_index = 0  # posisi bit pesan yang sedang disisipkan
    height, width, channels = image.shape  # ukuran gambar

    # menelusuri setiap pixel gambar
    for y in range(height):
        for x in range(width):

            # hanya menyisipkan pesan pada pixel yang termasuk area edge
            if edges[y, x] != 0:

                # menyisipkan bit ke 3 channel warna
                for c in range(3):

                    # jika masih ada bit pesan yang belum disisipkan
                    if data_index < len(binary_message):
                        pixel_value = int(image[y, x, c])

                        # menghapus LSB pixel, lalu menggantinya dengan bit pesan
                        image[y, x, c] = (pixel_value & 254) | int(binary_message[data_index])

                        # pindah ke bit pesan berikutnya
                        data_index += 1

                    # jika semua pesan sudah disisipkan, simpan gambar
                    if data_index >= len(binary_message):
                        cv2.imwrite(output_path, image)
                        return True

    # menyimpan gambar hasil steganografi
    cv2.imwrite(output_path, image)
    return True


# fungsi untuk mengambil pesan tersembunyi dari gambar
def extract_message_adaptive(image_path):
    # membaca gambar stego
    image = cv2.imread(image_path)

    # validasi jika gambar gagal dibaca
    if image is None:
        raise ValueError("Gambar tidak ditemukan.")

    # mendapatkan area edge yang sama seperti saat encode
    edges = get_edge_map(image)

    binary_data = ""  # menyimpan bit-bit hasil ekstraksi

    height, width, channels = image.shape

    # menelusuri setiap pixel gambar
    for y in range(height):
        for x in range(width):

            # hanya membaca pixel pada area edge
            if edges[y, x] != 0:

                # membaca 3 channel warna
                for c in range(3):

                    # mengambil bit terakhir dari pixel
                    binary_data += str(int(image[y, x, c]) & 1)

                    # setiap terkumpul 8 bit, coba ubah menjadi teks
                    if len(binary_data) % 8 == 0:
                        decoded_text = binary_to_text(binary_data)

                        # jika delimiter ditemukan, berarti pesan sudah selesai
                        if DELIMITER in decoded_text:
                            return decoded_text.replace(DELIMITER, "")

    # jika delimiter tidak ditemukan, berarti tidak ada pesan valid
    return None