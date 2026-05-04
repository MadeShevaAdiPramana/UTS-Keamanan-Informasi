import os
from flask import Flask, render_template, request, send_file

# import fungsi kriptografi (Vigenere)
from crypto import encrypt_vigenere, decrypt_vigenere

# import fungsi steganografi (Adaptive LSB)
from stego import embed_message_adaptive, extract_message_adaptive

# import fungsi evaluasi kualitas gambar
from metrics import calculate_psnr, calculate_ssim

# inisialisasi aplikasi Flask
app = Flask(__name__)

# folder untuk menyimpan file upload dan hasil output
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"

# memastikan folder ada (jika belum akan dibuat)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# route halaman utama
@app.route("/")
def index():
    return render_template("index.html", active_page="home")


# route utama untuk encode & decode (profile)
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":

        # ambil data dari form
        username = request.form.get("username", "")
        bio = request.form.get("bio", "")
        password = request.form.get("password", "")  # key Vigenere
        gender = request.form.get("gender", "male")  # mode (encode/decode)
        image = request.files.get("image")

        # validasi password tidak boleh kosong
        if not password.strip():
            return render_template(
                "profile.html",
                notification="Password cannot be empty.",
                notification_type="notification-error",
            )

        # validasi gambar harus diupload
        if not image or image.filename == "":
            return render_template(
                "profile.html",
                notification="Please upload a profile picture.",
                notification_type="notification-error",
            )

        # simpan gambar ke folder upload
        input_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(input_path)

        # FEMALE = ENCODE (menyisipkan pesan)
        if gender == "female":

            # validasi bio (pesan) tidak boleh kosong
            if not bio.strip():
                return render_template(
                    "profile.html",
                    notification="Bio cannot be empty.",
                    notification_type="notification-error",
                )

            # menentukan nama file output
            base_name = os.path.splitext(image.filename)[0]
            output_filename = "stego_" + base_name + ".png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            try:
                # 1. enkripsi pesan dengan Vigenere
                ciphertext = encrypt_vigenere(bio, password)

                # 2. sisipkan ciphertext ke gambar (Adaptive LSB)
                embed_message_adaptive(input_path, ciphertext, output_path)

            except ValueError as e:
                return render_template(
                    "profile.html",
                    notification=str(e),
                    notification_type="notification-error",
                )

            # hitung kualitas gambar setelah steganografi
            psnr = calculate_psnr(input_path, output_path)
            ssim = calculate_ssim(input_path, output_path)

            # tampilkan hasil encode
            return render_template(
                "profile.html",
                notification="Encode berhasil!",
                notification_type="notification-success",
                profile_image=output_path,
                output_filename=output_filename,
                psnr=round(psnr, 2),
                ssim=round(ssim, 4),
            )

        else:
            # MALE = DECODE (mengambil pesan)

            try:
                # 1. ekstrak ciphertext dari gambar
                extracted_ciphertext = extract_message_adaptive(input_path)

            except ValueError as e:
                return render_template(
                    "profile.html",
                    notification=str(e),
                    notification_type="notification-error",
                )

            # jika tidak ada pesan tersembunyi
            if extracted_ciphertext is None:
                return render_template(
                    "profile.html",
                    notification="Tidak ada pesan tersembunyi.",
                    notification_type="notification-error",
                )

            # 2. dekripsi ciphertext menjadi plaintext
            plaintext = decrypt_vigenere(extracted_ciphertext, password)

            # tampilkan hasil decode
            return render_template(
                "profile.html",
                notification="Decode berhasil!",
                notification_type="notification-info",
                bio=plaintext,
                profile_image=input_path,
            )

    # jika GET → tampilkan halaman
    return render_template("profile.html", active_page="profile")


# route untuk download hasil gambar stego
@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


# menjalankan aplikasi
if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)