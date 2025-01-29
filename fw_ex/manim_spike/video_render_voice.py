from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# pyright: reportWildcardImportFromLibrary=false
# pyright: reportMissingImports=false
# ruff: noqa: F403
# ruff: noqa: F405


class VideoAudioSyncScene(Scene):
    def construct(self):
        # Voiceover setup
        # self.set_speech_service(GTTSService(lang="en"))

        # Load video
        video = VideoMobject("sample_vid.mkv").scale(0.7)
        self.add(video)

        # Sync video with narration
        # with self.voiceover(
        #     text="This is a sample video synchronized with voice."
        # ) as tracker:
        self.play(video.play())
        self.wait(1)
