from manim import *
from manim_slides import Slide
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover import VoiceoverScene


# pyright: reportWildcardImportFromLibrary=false
# pyright: reportMissingImports=false
# ruff: noqa: F403
# ruff: noqa: F405


class ImageBackgroundSlide(Slide, VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))
        # Load background image
        bg_image = ImageMobject("jumpvalley.png").scale(2.5)
        bg_image.to_edge(ORIGIN)

        # Add the background image
        self.add(bg_image)

        # Title on top of the image
        title = Text("Welcome to Manim Presentation", color=WHITE).scale(0.8)
        title.to_edge(UP)
        # Add image and voiceover
        with self.voiceover(
            text="Slides are mixed with the audio to bring the best routine"
        ) as tracker:
            self.play(Write(title), run_time=tracker.duration)
            self.wait(2)
            self.next_slide()  # Move to next slide

        # Load background image
        bg_1 = ImageMobject("pagedata.png").scale(2)
        bg_1.to_edge(ORIGIN)

        # Add the background image
        self.add(bg_1)
        self.wait(2)
        # Add bullet points over the image background
        points = BulletedList("First Point", "Second Point", "Third Point", color=WHITE)
        with self.voiceover(
            text="Slides are discussing the theme of notion"
        ) as tracker:
            self.play(FadeIn(points), run_time=tracker.duration)
        self.wait(5)
        self.next_slide()
