# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydub",
# ]
# ///
import json
import sys
from pathlib import Path
from pydub import AudioSegment

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
        print("Usage: uv run generate_srt.py transcript.json input.mp3 output.srt")
        sys.exit(1)

    transcript_file = sys.argv[1]
    audio_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(transcript_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        transcript = data["transcription"]


    generate_srt(transcript, audio_file, output_file)
