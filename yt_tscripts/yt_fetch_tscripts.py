from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

video_id = input("Provide the Video_id: ")
# Must be a single transcript.
transcript = YouTubeTranscriptApi.get_transcript(video_id)


filename = f"{video_id}.txt"
# Now we can write it out to a file.
with open(filename, "w", encoding="utf-8") as json_file:
    for payload in transcript:
        print(payload["text"])
        json_file.write(f"{payload['start']} : {payload['text']}\n")
