# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydub",
#     "faster-whisper",
# ]
# ///

import json
import sys
from pathlib import Path
from pydub import AudioSegment
from faster_whisper import WhisperModel
import os

# Load Whisper model (you can choose size: tiny, base, small, medium, large)
model = WhisperModel("base", compute_type="auto")
tamil_model = WhisperModel("flyingleafe/faster-whisper-large-v3",
        device="cpu",          # change to "cuda" if you have GPU
        compute_type="int8",    # for CPU efficiency
    )

def transcribe(filepath):
    segments, _ = model.transcribe(filepath)

    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    return result   

def transcribe_tamil(filepath):
    segments, _ = tamil_model.transcribe(filepath, beam_size=5, language="ta")
    
    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    return result
   
def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    millis = int(seconds * 1000)
    hours = millis // (3600 * 1000)
    minutes = (millis % (3600 * 1000)) // (60 * 1000)
    secs = (millis % (60 * 1000)) // 1000
    ms = millis % 1000
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"

def generate_srt(transcript, audio_file, output_file):
    # Load audio for validation
    audio = AudioSegment.from_mp3(audio_file)
    duration_sec = len(audio) / 1000.0

    lines = []
    for i, entry in enumerate(transcript, start=1):
        start = entry["start"]
        end = entry["end"]
        text = entry["text"]

        # validate against audio length
        if end > duration_sec:
            print(f"Warning: Subtitle {i} ends after audio length, trimming to {duration_sec:.2f}s")
            end = duration_sec

        start_ts = format_timestamp(start)
        end_ts = format_timestamp(end)

        lines.append(f"{i}\n{start_ts} --> {end_ts}\n{text}\n")

    Path(output_file).write_text("\n".join(lines), encoding="utf-8")
    print(f"SRT file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: uv run mp3_to_srt.py ta input.mp3 output.srt")
        sys.exit(1)

    lang = sys.argv[1]
    audio_file = sys.argv[2]
    output_file = sys.argv[3]

    if lang == "ta":
        print("Selected Tamil Language.")
        transcript = transcribe_tamil(audio_file)
    else:
        print("Default is English Language")
        transcript = transcribe(audio_file)

    generate_srt(transcript, audio_file, output_file)
