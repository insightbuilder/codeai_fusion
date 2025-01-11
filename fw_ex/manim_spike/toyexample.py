# pyright: reportWildcardImportFromLibrary=false
# pyright: reportArgumentType=false
# ruff: noqa: F405
# ruff: noqa: F403

from manim import *


class ToyExample(Scene):
    def construct(self):
        orange_square = Square(color=ORANGE, fill_opacity=0.5)
        blue_circle = Circle(color=BLUE, fill_opacity=0.5)
        self.add(orange_square)
        self.play(ReplacementTransform(orange_square, blue_circle, run_time=3))
        small_dot = Dot(color=YELLOW, radius=0.1)
        small_dot.add_updater(lambda m: m.next_to(blue_circle, DOWN))
        self.play(Create(small_dot))
        self.play(blue_circle.animate.shift(RIGHT))
        self.wait()
        self.play(FadeOut(small_dot, blue_circle))
