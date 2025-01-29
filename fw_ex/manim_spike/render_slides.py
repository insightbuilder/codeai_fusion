from manim import *
from manim_slides import Slide


# pyright: reportWildcardImportFromLibrary=false
# pyright: reportMissingImports=false
# ruff: noqa: F403
# ruff: noqa: F405


class ImageBackgroundSlide(Slide, Scene):
    def construct(self):
        # Load background image
        bg_image = ImageMobject("jumpvalley.png").scale(2)
        bg_image.to_edge(ORIGIN)

        # Add the background image
        self.add(bg_image)

        # Title on top of the image
        title = Text("Welcome to Manim Presentation", color=WHITE).scale(0.8)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(2)
        self.next_slide()  # Move to next slide

        # Load background image
        bg_1 = ImageMobject("pagedata.png").scale(2)
        bg_1.to_edge(ORIGIN)

        # Add the background image
        self.add(bg_1)
        self.wait(2)
        # Add bullet points over the image background
        points = BulletedList("First Point", "Second Point", "Third Point", color=WHITE)
        self.play(FadeIn(points))
        self.wait(5)
        self.next_slide()
