from flask import Flask, request, session, jsonify
from werkzeug.utils import secure_filename


def upload_file():
    if "user_id" not in session:
        return "User not logged in", 401

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    file_type = request.form.get("type")  # 'protein' or 'toxin'

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)

        # Store filename in session
        session[f"{file_type}_filename"] = filename
        return (
            jsonify({"message": "File uploaded successfully", "filename": filename}),
            200,
        )
