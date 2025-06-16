# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "moviepy",
#     "faster_whisper",
#     "pydub",
#     "onnxruntime",
#     "prompt_toolkit",
#     "openai",
#     "requests"
# ]
# ///

from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from pathlib import Path
from auto_transcript_extract import (
    extract_segments,
    extract_kecs,
    search_and_download_pexels_videos,
)

if __name__ == "__main__":
    completer = PathCompleter(only_directories=False)
    path = prompt("File: ", completer=completer)

    if path.lower().endswith(".txt") and Path(path).exists():
        with open(path, "r") as f:
            transcript = f.read()
            segments = extract_segments(transcript)
            print("Got the Segments of scenes. Extracting Key words.")
            if segments.logicalparts:
                for segment in segments.logicalparts:
                    scenes = extract_kecs(segment)
                    print(scenes)
                    # break
                    if scenes.kecs:
                        search_and_download_pexels_videos(scenes.kecs, max_per_term=1)
                    # break
            else:
                print("No logical parts found in the transcript.")
    else:
        print("Invalid or non-existent file.")
