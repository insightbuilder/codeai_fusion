from moviepy import * # type: ignore
 
txt = TextClip(font="Bebas-Regular.ttf", text="Hello", font_size=140, color="white")
there = TextClip(font="Bebas-Regular.ttf", text="There", font_size=140, color="yellow")
hru = TextClip(font="Bebas-Regular.ttf", text="How are you", font_size=140, color="red")

txt = txt.with_duration(5).with_effects([vfx.CrossFadeIn(1)]).with_position((45, 20))
there = there.with_duration(5).with_effects([vfx.CrossFadeIn(1)]).with_position((345, 20))
hru = hru.with_duration(5).with_effects([vfx.CrossFadeIn(1)]).with_position((45, 150))

bg = VideoFileClip("registration.mp4")

video = CompositeVideoClip([bg, txt, there, hru])

video.write_videofile("simple_vid.mp4", fps=30)