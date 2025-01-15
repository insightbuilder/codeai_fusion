# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class MasterParts(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = ORANGE
        LEFT_SIDE = self.camera.frame_width * LEFT / 2
        RIGHT_SIDE = self.camera.frame_width * RIGHT / 2
        # print(LEFT)
        # print(LEFT_SIDE)
        # print(RIGHT)
        # print(RIGHT_SIDE)
        # Title and Author
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
        text_kwargs = {"font_size": 80, "color": BLACK, "weight": BOLD}
        future_kwargs = {"font_size": 100, "color": BLACK, "weight": BOLD}
        shape_your = Text("Master the Parts", **text_kwargs)
        future = Text("Whole", **future_kwargs)
        with_thots = Text("Will make Itself", **text_kwargs)

        shape_your.move_to(UP * 1.2)
        with_thots.move_to(DOWN * 1.3)

        # Animations
        self.play(Create(top_line), Create(bottom_line), run_time=1.5)
        self.wait(1.5)

        self.add(title, author)
        self.play(
            GrowFromCenter(shape_your),
            GrowFromCenter(future),
            GrowFromCenter(with_thots),
            run_time=2.5,
        )
        self.wait(2.5)
