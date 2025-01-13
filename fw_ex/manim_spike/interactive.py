from manimlib import *

# pyright: reportMissingImports=false
# pyright: reportWildcardImportFromLibrary=false
# ruff: noqa: F405
# ruff: noqa: F403


class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.interactive_embed()


# scene = MyScene()
# scene.render()
# scene.interactive_embed()  # Opens interactive mode
