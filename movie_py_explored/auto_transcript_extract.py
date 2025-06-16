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

from moviepy import VideoFileClip
from faster_whisper import WhisperModel
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from pathlib import Path
import openai

import requests
import os

from pydantic import BaseModel
from typing import List

from uuid import uuid4


class ScriptSegment(BaseModel):
    scene: str
    kecs: List[str]


class Segment(BaseModel):
    logicalparts: List[str]


PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")  # Set this in your environment
PEXELS_SEARCH_URL = "https://api.pexels.com/videos/search"

HEADERS = {"Authorization": PEXELS_API_KEY}


def search_and_download_pexels_videos(
    kecs, output_dir="pexels_downloads", max_per_term=2
):
    os.makedirs(output_dir, exist_ok=True)

    for term in kecs:
        print(f"\n🔍 Searching Pexels for: {term}")
        params = {"query": term, "per_page": max_per_term}
        response = requests.get(PEXELS_SEARCH_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"❌ Error searching '{term}': {response.text}")
            continue

        videos = response.json().get("videos", [])
        for video in videos:
            url = video["video_files"][0]["link"]
            ext = url.split("?")[0].split(".")[-1]
            idx = str(uuid4())[:4]
            filename = f"{term.replace(' ', '_')}_{idx}.{ext}"

            print(f"⬇️ Downloading: {filename}")
            vid_data = requests.get(url)
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(vid_data.content)


def select_mp4_file():
    print("Enter path to .mp4 file (Tab to autocomplete):")
    completer = PathCompleter(only_directories=False)
    path = prompt("File: ", completer=completer)

    if path.lower().endswith(".mp4") and Path(path).exists():
        return path
    else:
        print("Invalid or non-existent file.")
        return None


def extract_audio(mp4_path, audio_path="extracted_audio.wav"):
    video = VideoFileClip(mp4_path)
    video.audio.write_audiofile(audio_path, codec="pcm_s16le")  # saves as WAV
    return audio_path


def transcribe(audio_path, model_size="base"):
    model = WhisperModel(
        model_size, compute_type="int8"
    )  # use "float16" if you have GPU
    segments, _ = model.transcribe(audio_path)

    transcript = ""
    for segment in segments:
        transcript += f"{segment.text.strip()} "
    return transcript.strip()


def write_transcript(transcript, transcript_file="transcript.txt"):
    with open(transcript_file, "w") as f:
        f.write(transcript)


def extract_segments(transcript: str):
    SYSTEM_PROMPT = """
You are a script analysis tool. Given a transcript, break it down into logical parts like scenes or topic sections of a script.
return:
- logicalparts: a list of parts from the given transcript.

Only respond in the provided JSON schema. No explanation.
"""

    client = openai.OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.5,
        response_format=Segment,
    )

    return response.choices[0].message.parsed


def extract_kecs(scene: str):
    SYSTEM_PROMPT = """
You are a script analysis tool. Given a scene you have to provide the visual search keywords.
return:
- scene: the given scene 
- kecs: a list of 3 visual search keywords (KECs) that best represent the scene. Don't include character names, or other PIIs.

Only respond in the provided JSON schema. No explanation.
"""

    client = openai.OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"The given scene is: {scene}"},
        ],
        temperature=0.5,
        response_format=ScriptSegment,
    )

    return response.choices[0].message.parsed


if __name__ == "__main__":
    mp4_path = select_mp4_file()
    if not mp4_path:
        exit()

    print(f"Selected: {mp4_path}")
    audio_path = extract_audio(mp4_path)

    print("Transcribing...")
    transcript = transcribe(audio_path)

    print("\n--- Transcript ---\n")
    print(transcript)
    write_transcript(transcript)
