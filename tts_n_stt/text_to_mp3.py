# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydub",
#     "pyttsx3",
# ]
# ///
import pyttsx3
from pydub import AudioSegment

# Initialize TTS engine
engine = pyttsx3.init()

# Two spoken sentences
text = "An apple is a sweet fruit that comes in many colors like red, green, and yellow. Apples are rich in fiber and vitamins, and are enjoyed worldwide."

# Save to WAV first (pyttsx3 works best with wav)
engine.save_to_file(text, "apple_description.wav")
engine.runAndWait()

# Convert to MP3 using pydub
sound = AudioSegment.from_wav("apple_description.wav")
sound.export("apple_description.mp3", format="mp3")

print("Generated apple_description.mp3")