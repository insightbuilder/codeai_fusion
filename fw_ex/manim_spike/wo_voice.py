from manim import *


class GTTSExample(Scene):
    def construct(self):
        circle = Circle()
        square = Square().shift(2 * RIGHT)

        self.play(Create(circle))

        self.play(circle.animate.shift(2 * LEFT))

        self.play(Transform(circle, square))

        self.play(Uncreate(circle))

        self.wait()
