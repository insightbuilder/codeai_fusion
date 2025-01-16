# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false
# ruff: noqa: F405
# ruff: noqa: F403

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


config.pixel_height = 1920  # YouTube Shorts vertical resolution
config.pixel_width = 1080  # Standard width
config.frame_height = 14  # Adjust based on object positioning
config.frame_width = 7.875  # Keep the aspect ratio 9:16


class YouTubeScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        text = Text("Manim Shorts!", font_size=80).to_edge(UP)
        square = Square().scale(2).set_color(BLUE)
        with self.voiceover(
            text="We are creating text and shapes in YT format!"
        ) as tracker:
            self.play(Write(text), run_time=tracker.duration)
            self.play(Create(square), run_time=tracker.duration)
            self.wait()
        with self.voiceover(text="The Shapes are being rotated now") as tracker:
            self.play(square.animate.rotate(PI / 4), run_time=tracker.duration)
            self.wait()
        with self.voiceover(text="Now, let's remove them!") as tracker:
            self.play(FadeOut(text, square), run_time=tracker.duration)
            self.wait()
