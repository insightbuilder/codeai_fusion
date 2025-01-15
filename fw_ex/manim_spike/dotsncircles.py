from manim import *

# pyright: reportWildcardImportFromLibrary=false
# ruff: noqa: F405
# ruff: noqa: F403


class DotsNCircles(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(5)])
        circles = VGroup(*[Circle() for _ in range(5)])
        dots.arrange(RIGHT)
        circles.arrange(DOWN)
        self.add(dots, circles)

        # lets animate them together
        self.play(ReplacementTransform(dots, circles), run_time=2)
        self.wait()
        newdots = VGroup(*[Dot() for _ in range(5)])
        self.add(newdots)
        self.wait()
        self.play(Create(newdots.arrange(UP)), run_time=2)
