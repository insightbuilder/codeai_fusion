# pyright: reportUnknownMemberType=false
# pyright: reportMissingImports=false
# pyright: reportWildcardImportFromLibrary=false
# pyright: reportArgumentType=false
# ruff: noqa: F405
# ruff: noqa: F403

from manim import *


class TextTuto(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = Text("Text Tuto", font_size=40, weight=BOLD, color=BLACK)
        title.to_edge(UP)
        self.add(title)
        stars = VGroup(*[
            Star(color=RED, inner_radius=0.1, outer_radius=0.2) for _ in range(5)
        ])
        stars.arrange(DOWN)
        stars.shift(LEFT * 2)
        dots = VGroup(*[Dot(color=BLACK, radius=0.2) for _ in range(5)])
        dots.arrange(DOWN)
        texts = VGroup(*[
            Text(f"This is part {i}", font_size=15, color=BLACK) for i in range(5)
        ])
        texts.arrange(DOWN * 1.5)
        texts.next_to(stars, RIGHT)
        dots.next_to(texts, RIGHT)
        self.play(Create(stars))
        self.play(GrowFromCenter(texts), run_time=2)
        self.wait()
        self.add(dots)
        self.wait()
