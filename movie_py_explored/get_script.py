from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from faster_whisper import WhisperModel

# Load video and extract audio
video = VideoFileClip("./sales_training_awareness_src.mp4")
video.audio.write_audiofile("sales_training_awareness.wav") # type: ignore

# Transcribe with faster-whisper
model = WhisperModel("small")  # You can use 'small' or 'medium' if needed
segments, _ = model.transcribe("sales_training_awareness.wav")
# print(f"Segments are: {segments}")

# Build typewriter subtitles for all segments
subtitle_clips = []
with open("subtitle.srt", 'w') as fsrt:
    for idx, segment in enumerate(segments):
        fsrt.write(f"{segment.text} : {segment.start}, {segment.end - segment.start}")
        subtitle_clips.append([segment.text, segment.start, segment.end - segment.start])
        if idx % 5 == 0:
            print(f"At idx: {idx}")
            break


print("Writing Extracted Subtitle:")
print(subtitle_clips)