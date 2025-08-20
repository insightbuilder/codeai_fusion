The folder contains the python servers for both
Text to Speech and Speech to Text conversion. The
scripts use uv package manager for dependencies.
You can refer to this youtube video for more
details: https://youtu.be/LZXps8KE4XM

## Text to Speech with Kokoro Model:

The kokorotts models has to be downloaded for the
app.py to work.

wget
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx

wget
https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

The app.py file is the Text to Speech Gradio
server. Run it with below command

uv run app.py

The onnx and bin files are not commited to the
repo. So you have to download it.

## Speech to Text with Whisper Model:

The stt_app.py is the Speech to Text Flask Server.
Run it with below command

uv run stt_app.py

## text to speech with simpler pydub

- text_to_mp3.py gives the speech file 

- Use the above to get synthetic speech, which is then used for speech to text in json format using stt_app.py(use mp3_to_srt.py directly)

- subtitles.srt is recieved in JSon Format. renamed it

## Use the mp3 to SRT converter using mp3_to_srt.py:

Ideally you will have your mp3 file. You will want to transcribe that. 

- uv run mp3_to_srt.py your_voice.mp3 description_subs.srt

The above command will do the needful.

