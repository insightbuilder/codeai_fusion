from manim import *

# pyright: reportWildcardImportFromLibrary=false
# pyright: reportArgumentType=false
# ruff: noqa: F405
# ruff: noqa: F403


class AddBullets(Scene):
    def construct(self):
        title = Text("Add Bullets")
        title.move_to(4 * UP)
        self.play(Write(title))
