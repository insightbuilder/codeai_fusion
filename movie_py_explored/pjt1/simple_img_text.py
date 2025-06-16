from moviepy import * # type: ignore
 
txt = TextClip(font="Bebas-Regular.ttf", text="Hello", font_size=400, color="white")
there = TextClip(font="Bebas-Regular.ttf", text="There", font_size=400, color="green")
hru = TextClip(font="Bebas-Regular.ttf", text="How are you", font_size=400, color="green")

txt = txt.with_duration(5).with_effects([vfx.SlideIn(1, "left")]).with_position((45, 100))
there = there.with_duration(5).with_effects([vfx.SlideIn(1, "left")]).with_position((745, 100))
hru = hru.with_duration(5).with_effects([vfx.SlideIn(1, "left")]).with_position((45, 500))

bg = ImageClip("pjt_bg.png").with_duration(5)

video = CompositeVideoClip([bg, txt, there, hru])

video.write_videofile("simple.mp4", fps=5)