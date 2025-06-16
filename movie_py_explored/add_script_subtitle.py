from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from faster_whisper import WhisperModel

def typewriter_subtitle(text, start, duration, fontsize=42, color='black'):
    clips = []
    total_chars = len(text)
    if total_chars == 0:
        return []

    char_duration = duration / total_chars

    for i in range(1, total_chars + 1):
        txt = text[:i] + "|" if i < total_chars else text[:i]  # Blinking cursor
        txt_clip = (
            TextClip(font="./fonts/font.ttf", text=txt, font_size=fontsize, color=color)
            .with_position(("center", "bottom"))
            .with_start(start + (i - 1) * char_duration)
            .with_duration(char_duration)
        )
        clips.append(txt_clip)

    return clips


# Load video and extract audio
video = VideoFileClip("./results/auto_edit.mp4")
video.audio.write_audiofile("auto_audio.wav")

# Transcribe with faster-whisper
model = WhisperModel("base")  # You can use 'small' or 'medium' if needed
segments, _ = model.transcribe("auto_audio.wav")
print(f"Segments are: {segments}")

# Build typewriter subtitles for all segments
subtitle_clips = []
for segment in segments:
    typing_clips = typewriter_subtitle(
        segment.text, segment.start, segment.end - segment.start
    )
    subtitle_clips.extend(typing_clips)

print("Writing Final Video with Subtitle...")

# Final composite
final = CompositeVideoClip([video, *subtitle_clips])
final.write_videofile("./results/typewriter_subtitles.mp4", fps=24)