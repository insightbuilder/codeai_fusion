from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# pyright: reportWildcardImportFromLibrary=false
# pyright: reportMissingImports=false
# ruff: noqa: F403
# ruff: noqa: F405


class ImageWithVoiceover(VoiceoverScene):
    def construct(self):
        # Set up voiceover service
        self.set_speech_service(GTTSService(lang="en"))

        # Load image
        image = ImageMobject("jumpvalley.png").scale(1.5)
        image.to_edge(UP)

        # Add image and voiceover
        with self.voiceover(
            text="Here is an image presented for discussion."
        ) as tracker:
            self.add(image)
            self.wait(tracker.duration)
