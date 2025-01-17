# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class LogicCode(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = ORANGE
        LEFT_SIDE = self.camera.frame_width * LEFT / 2
        RIGHT_SIDE = self.camera.frame_width * RIGHT / 2
        # Title and Author
        title = Text("Positivity With Python", font_size=30, weight=BOLD, color=BLACK)
        title.to_corner(UL)
        author = Text("KamalRaj", font_size=30, weight=BOLD, color=BLACK)
        author.to_corner(DR)
        top_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        top_line.to_edge(UP, buff=0.3)
        bottom_line = Line(LEFT_SIDE, RIGHT_SIDE, color=BLACK)
        bottom_line.to_edge(DOWN, buff=0.3)
        # Main text
        text_kwargs = {"font_size": 80, "color": BLACK, "weight": BOLD}
        do_more = Text("Make the Code", **text_kwargs)
        ask_more = Text("SPEAK", **text_kwargs)
        do_more.move_to(UP * 0.8)
        ask_more.move_to(DOWN * 0.8)
        self.play(Create(top_line), Create(bottom_line), run_time=1.5)
        self.add(
            title,
            author,
        )
        self.play(GrowFromCenter(do_more), GrowFromCenter(ask_more), run_time=2.5)
        self.wait(2.5)
