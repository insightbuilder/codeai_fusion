# pyright: reportWildcardImportFromLibrary=false
# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
# ruff: noqa: F401

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import sys

# print("sys argv", sys.argv)
config.pixel_height = 1920
config.frame_width = 1080
config.frame_height = 14
config.frame_width = 7.875


class AVidImg(VoiceoverScene):
    def construct(self):
        # Set background Audio
        self.set_speech_service(GTTSService(lang="en", tld="com"))

        # Set background color
        self.camera.background_color = ORANGE
        LEFT_SIDE = self.camera.frame_width * LEFT / 2
        RIGHT_SIDE = self.camera.frame_width * RIGHT / 2
        title = Text("Positivity With Python", font_size=30, weight=BOLD, color=BLACK)
        title.to_corner(UL)

        author = Text("KamalRaj", font_size=30, weight=BOLD, color=BLACK)
        author.to_corner(DR)

        # Top line (Starts from right edge of title and extends to right side of frame)
        top_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        top_line.to_edge(UP, buff=0.3)

        # Bottom line (Full width)
        bottom_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        bottom_line.to_edge(DOWN, buff=0.3)

        # Main text
        text_kwargs = {"font_size": 40, "color": BLACK, "weight": BOLD}
        future_kwargs = {"font_size": 50, "color": BLACK, "weight": BOLD}

        # Audio Content
        global audio_text  # using this to send the audio data in
        with open("/home/uberdev/audio_text.txt", "r") as aud:
            audio_text = aud.read()

        if len(sys.argv) == 6:
            print(sys.argv[3], sys.argv[4], sys.argv[5])
            cm = Text(sys.argv[3], **text_kwargs)
            mid = Text(sys.argv[4], **text_kwargs)
            st = Text(sys.argv[5], **future_kwargs)

            cm.move_to(UP * 1.4)
            st.move_to(DOWN * 1.6)
            self.play(Create(top_line), Create(bottom_line), run_time=1.5)
            self.add(title, author)
            with self.voiceover(text=audio_text) as tracker:
                self.play(
                    GrowFromCenter(cm),
                    GrowFromCenter(mid),
                    GrowFromCenter(st),
                    run_time=tracker.duration * 0.25,
                )
                self.wait(tracker.duration * 0.75)
        else:
            print(sys.argv[3], sys.argv[4])
            cm = Text(sys.argv[3], **text_kwargs)
            st = Text(sys.argv[4], **future_kwargs)

            cm.move_to(UP)
            st.move_to(DOWN)
            # Animations
            self.play(Create(top_line), Create(bottom_line), run_time=1.5)

            self.add(title, author)
            with self.voiceover(text=audio_text) as tracker:
                self.play(
                    GrowFromCenter(cm),
                    GrowFromCenter(st),
                    run_time=tracker.duration * 0.25,
                )
                self.wait(tracker.duration * 0.75)
