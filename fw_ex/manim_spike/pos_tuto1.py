# pyright: reportWildcardImportFromLibrary=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalOperand=false
# pyright: reportArgumentType=false

# ruff: noqa: F405
# ruff: noqa: F403
from manim import *


class PosTuto(Scene):
    def construct(self):
        left_sqr = Square(color=BLUE, fill_opacity=0.5).shift(2 * LEFT)
        right_sqr = Square(color=YELLOW, fill_opacity=0.5).shift(2 * RIGHT)

        self.add(left_sqr, right_sqr)

        left_sqr.move_to(RIGHT)
        right_sqr.to_corner(UR)

        self.play(right_sqr.animate.move_to(ORIGIN))
        self.wait(1)
        self.play(right_sqr.animate.move_to(DL))
        self.play(left_sqr.animate.move_to(UL))
        self.wait(1)
        self.play(right_sqr.animate.move_to(DL * 2))
        self.play(left_sqr.animate.move_to(UL * 3))
        self.wait()
        l_text = Text("Left", color=BLUE).to_corner(LEFT)
        r_text = Text("Right", color=YELLOW).move_to(RIGHT)
        self.add(l_text, r_text)
        self.wait(5)
        self.play(l_text.animate.to_edge(RIGHT), run_time=3)
        self.play(l_text.animate.to_edge(UP), run_time=3)
        self.wait()
        self.play(r_text.animate.next_to(l_text, LEFT, buff=0.3))
        self.wait()
