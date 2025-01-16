# pyright: reportMissingImports=false
# pyright: reportWildcardImportFromLibrary=false
# pyright: reportArgumentType=false
# ruff: noqa: F405
# ruff: noqa: F403

from manim import *


class LineTuto1(Scene):
    def construct(self):
        line = Line(LEFT * 2, RIGHT * 2)
        linever = Line(UP * 2, DOWN * 2)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1])
        self.add(ax)
        self.play(Create(line), Create(linever), run_time=3)
        a3x = Axes(x_range=[0, 20, 1], y_range=[0, 15, 1])
        # NumberPlane().add_coordinates()
        # self.play(Uncreate(ax), Create(a3x), run_time=2)
        self.wait(2)
        line.move_to([-1, 0, 0])
        linever.move_to([-1, -1, 0])
        self.play(Uncreate(line), Uncreate(linever), run_time=3)
        self.wait(2)
