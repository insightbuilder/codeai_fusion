from moviepy import * # type: ignore

# load video and take clips between 5 to 12 sec
clip = VideoFileClip("./example_vids/wisdom.mp4").subclipped(5, 12)

clip = clip.with_volume_scaled(0.8) # volume reduced

txt_clp = TextClip(font="./fonts/Lato/Lato-Bold.ttf",
    text="Wisdom in Automation",
    font_size = 70,
    color="black")

txt_clp = txt_clp.with_position("center").with_duration(7)

video = CompositeVideoClip([clip, txt_clp])

video.write_videofile("./results/quick_ppt.mp4",)