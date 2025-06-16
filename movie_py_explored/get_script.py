from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from faster_whisper import WhisperModel
from tqdm import tqdm 

# Load video and extract audio
video = VideoFileClip("./sales_training_awareness_src.mp4")
video.audio.write_audiofile("auto_edit.wav") # type: ignore

# Transcribe with faster-whisper
model = WhisperModel("small")  # You can use 'small' or 'medium' if needed
# model_v2 = WhisperModel("large-v2") # when using tamil 
segments, _ = model.transcribe("auto_edit.wav")
# when using tamil
# segments, _ = model_v2.transcribe("/content/training_tamil.wav", language="ta")

# segments are lazy generators, so executing below line will take long time
# Avoid background music, poor mics, or mixed language
segments = list(tqdm(segments))  # Shows a progress bar

# Build typewriter subtitles for all segments
subtitle_clips = []
with open("subtitle.srt", 'w') as fsrt:
    for idx, segment in enumerate(segments):
        fsrt.write(f"{segment.text} : {segment.start}, {segment.end - segment.start}")
        subtitle_clips.append([segment.text, segment.start, segment.end - segment.start])


print("Writing Extracted Subtitle:")
print(subtitle_clips)