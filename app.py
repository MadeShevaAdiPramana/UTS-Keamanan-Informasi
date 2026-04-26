import os
from flask import Flask, render_template, request, send_file

from crypto import encrypt_vigenere, decrypt_vigenere
from stego import embed_message_adaptive, extract_message_adaptive
from metrics import calculate_psnr, calculate_ssim

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == "POST":
        image = request.files["image"]
        message = request.form["message"]
        key = request.form["key"]

        if not key.strip():
            return render_template(
                "encode.html",
                result=False,
                error="Key tidak boleh kosong."
            )

        input_path = os.path.join(UPLOAD_FOLDER, image.filename)

        base_name = os.path.splitext(image.filename)[0]
        output_filename = "stego_" + base_name + ".png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        image.save(input_path)

        ciphertext = encrypt_vigenere(message, key)
        embed_message_adaptive(input_path, ciphertext, output_path)

        psnr = calculate_psnr(input_path, output_path)
        ssim = calculate_ssim(input_path, output_path)

        return render_template(
            "encode.html",
            result=True,
            output_image=output_path,
            output_filename=output_filename,
            psnr=round(psnr, 2),
            ssim=round(ssim, 4)
        )

    return render_template("encode.html", result=False)


@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == "POST":
        image = request.files["image"]
        key = request.form["key"]

        if not key.strip():
            return render_template(
                "decode.html",
                result=True,
                message="Key tidak boleh kosong."
            )

        input_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(input_path)

        extracted_ciphertext = extract_message_adaptive(input_path)

        if extracted_ciphertext is None:
            return render_template(
                "decode.html",
                result=True,
                message="Pesan tidak ditemukan. Pastikan file yang diupload adalah stego image PNG hasil encode."
            )

        plaintext = decrypt_vigenere(extracted_ciphertext, key)

        return render_template(
            "decode.html",
            result=True,
            message=plaintext
        )

    return render_template("decode.html", result=False)


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)