# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "faster-whisper",
#     "flask",
# ]
# ///
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import os

app = Flask(__name__)

# Load Whisper model (you can choose size: tiny, base, small, medium, large)
model = WhisperModel("base", compute_type="auto")

@app.route("/")
def index():
    return "Whisper Transcription API is running."

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save file temporarily
    filepath = os.path.join("/tmp", file.filename)
    file.save(filepath)

    segments, _ = model.transcribe(filepath)

    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    os.remove(filepath)  # clean up

    return jsonify({"transcription": result})

if __name__ == "__main__":
    app.run(debug=True, port=8000)

