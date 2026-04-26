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
    return render_template("index.html", active_page="home")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        username = request.form.get("username", "")
        bio = request.form.get("bio", "")
        password = request.form.get("password", "")
        gender = request.form.get("gender", "male")
        image = request.files.get("image")

        # Validate: password (Vigenère key) must not be empty
        if not password.strip():
            return render_template(
                "profile.html",
                active_page="profile",
                notification="Password cannot be empty.",
                notification_type="notification-error",
                username=username,
                bio=bio,
                password=password,
                mode=gender,
            )

        # Validate: an image must be uploaded
        if not image or image.filename == "":
            return render_template(
                "profile.html",
                active_page="profile",
                notification="Please upload a profile picture.",
                notification_type="notification-error",
                username=username,
                bio=bio,
                password=password,
                mode=gender,
            )

        input_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(input_path)

        # Female = Encode, Male = Decode
        if gender == "female":
            # --- ENCODE ---
            if not bio.strip():
                return render_template(
                    "profile.html",
                    active_page="profile",
                    notification="Bio cannot be empty when saving a profile.",
                    notification_type="notification-error",
                    username=username,
                    bio=bio,
                    password=password,
                    mode=gender,
                )

            base_name = os.path.splitext(image.filename)[0]
            output_filename = "stego_" + base_name + ".png"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            try:
                ciphertext = encrypt_vigenere(bio, password)
                embed_message_adaptive(input_path, ciphertext, output_path)
            except ValueError as e:
                return render_template(
                    "profile.html",
                    active_page="profile",
                    notification=str(e),
                    notification_type="notification-error",
                    username=username,
                    bio=bio,
                    password=password,
                    mode=gender,
                )

            psnr = calculate_psnr(input_path, output_path)
            ssim = calculate_ssim(input_path, output_path)

            return render_template(
                "profile.html",
                active_page="profile",
                notification="Profile updated successfully!",
                notification_type="notification-success",
                username=username,
                bio=bio,
                password=password,
                mode=gender,
                profile_image=output_path,
                output_filename=output_filename,
                show_analytics=True,
                psnr=round(psnr, 2),
                ssim=round(ssim, 4),
            )

        else:
            # --- DECODE ---
            try:
                extracted_ciphertext = extract_message_adaptive(input_path)
            except ValueError as e:
                return render_template(
                    "profile.html",
                    active_page="profile",
                    notification=str(e),
                    notification_type="notification-error",
                    username=username,
                    bio=bio,
                    password=password,
                    mode=gender,
                )

            if extracted_ciphertext is None:
                return render_template(
                    "profile.html",
                    active_page="profile",
                    notification="No hidden data found in this image. Please upload a valid profile picture.",
                    notification_type="notification-error",
                    username=username,
                    bio=bio,
                    password=password,
                    mode=gender,
                )

            plaintext = decrypt_vigenere(extracted_ciphertext, password)

            return render_template(
                "profile.html",
                active_page="profile",
                notification="Profile loaded successfully! Your bio has been updated.",
                notification_type="notification-info",
                username=username,
                bio=plaintext,
                password=password,
                mode=gender,
                profile_image=input_path,
            )

    return render_template("profile.html", active_page="profile")


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)