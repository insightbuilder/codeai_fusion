from moviepy import *

bbbclip = VideoFileClip("./example_vids/bbb.mp4").subclipped(0, -96)

txt_clp = TextClip(font="./fonts/font.ttf",
                   text="Getting Hang of this",
                   font_size=70,
                   color='black')

txt_clp = txt_clp.with_position(("center", "top")).with_duration(15)

video_cutout = CompositeVideoClip([bbbclip, txt_clp])

video_cutout.write_videofile("./results/bbb_cutout.mp4")