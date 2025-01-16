# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class FeelCode(Scene):
    def construct(self):
        self.camera.background_color = ORANGE
        LEFT_SIDE = self.camera.frame_width * LEFT / 2
        RIGHT_SIDE = self.camera.frame_width * RIGHT / 2
        print("Left: {LEFT}, Right: {RIGHT}".format(LEFT=LEFT, RIGHT=RIGHT))

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

        # Main Text
        text_kwargs = {"font_size": 80, "color": BLACK, "weight": BOLD}
        feel_code = Text("Feel The Code", **text_kwargs)

        self.add(title, author, top_line, bottom_line)
        self.play(GrowFromCenter(feel_code))
        self.wait(2.5)
