from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Route to upload a file via POST request
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return jsonify({
            "message": f"File {file.filename} uploaded successfully",
            "filepath": filepath,
        }), 201


# Route to download the uploaded file via GET request
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    try:
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], filename, as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
