# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class DoOnce(Scene):
    def construct(self):
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
        text_kwargs = {"font_size": 80, "color": BLACK, "weight": BOLD}
        future_kwargs = {"font_size": 100, "color": BLACK, "weight": BOLD}
        doonce = Text("Do Once", **text_kwargs)
        designonce = Text("Design Once", **text_kwargs)
        automate = Text("Automate", **future_kwargs)

        doonce.move_to(UP * 1.8)
        automate.move_to(DOWN * 1.8)

        # Animations
        self.play(Create(top_line), Create(bottom_line), run_time=1.5)

        self.add(title, author)
        self.play(
            GrowFromCenter(doonce),
            GrowFromCenter(designonce),
            GrowFromCenter(automate),
            run_time=2.5,
        )
        self.wait(2.5)
