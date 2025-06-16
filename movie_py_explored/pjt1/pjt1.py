from moviepy import * # type: ignore
import numpy as np

# starts with image clip

bg_image = ImageClip("pjt_bg.png").with_duration(110)

# bg_image.preview(fps=10)

topic_expl_list = [
    "Studying in top U.S. institutions connects you with motivated, driven peers—your future collaborators, co-founders, and lifelong professional network.",
    "Alumni from top universities often occupy leadership roles across industries, offering mentorship, referrals, and career opportunities for new graduates.",
    "Graduates from U.S. institutions often land jobs with competitive starting packages, thanks to strong brand value and skill-based training.",
    "The culture encourages excellence, critical thinking, and resilience—building the mindset that high performers and leaders thrive on.",
    "Students get access to real-world, high-impact projects through research labs, industry tie-ups, and team-based coursework.",
    "Top U.S. campuses are startup-friendly environments, with incubators, funding access, and mentors helping students turn ideas into companies.",
    "Programs like OPT and STEM extensions offer a legal path to work in the U.S. post-graduation, with higher chances of H1B sponsorship.",
    "Diverse campuses offer global perspectives, improving communication, empathy, and adaptability—skills essential in today’s world."
]
topics_list = [""
"1) Network of high performance students",
"2) Strong Alumni of the college",
"3) Getting Higher starting salary",
"4) Mindset of high achiever",
"5) Working on high value project",
"6) Innovation Hubs and Startups",
"7) Higher Chances US Visa",
"8) Exposure to different cultures"
]

# Use method='label' (faster but single-line only):

topic_clips = [TextClip(font="Bebas-Regular.ttf",
                        text=tp,
                        font_size=175,
                        color='white', 
                        method="label") for tp in topics_list]

topic_clips[0] = topic_clips[0].with_position((45, 100))
topic_clips[1] = topic_clips[1].with_position((45, 250))
topic_clips[2] = topic_clips[2].with_position((45, 400))
topic_clips[3] = topic_clips[3].with_position((45, 550))
topic_clips[4] = topic_clips[4].with_position((45, 650))
topic_clips[5] = topic_clips[5].with_position((45, 750))
topic_clips[6] = topic_clips[6].with_position((45, 850))
topic_clips[7] = topic_clips[7].with_position((45, 950))

topic_clips[0] = topic_clips[0].with_start(5).with_end(bg_image.end)
topic_clips[1] = topic_clips[1].with_start(17).with_end(bg_image.end)
topic_clips[2] = topic_clips[2].with_start(29).with_end(bg_image.end)
topic_clips[3] = topic_clips[3].with_start(41).with_end(bg_image.end)
topic_clips[4] = topic_clips[4].with_start(53).with_end(bg_image.end)
topic_clips[5] = topic_clips[5].with_start(65).with_end(bg_image.end)
topic_clips[6] = topic_clips[6].with_start(77).with_end(bg_image.end)
topic_clips[7] = topic_clips[7].with_start(89).with_end(bg_image.end)

# print("Topic 1 start:", topic_clips[7].start)

topic_clips[0] = topic_clips[0].with_effects([vfx.CrossFadeIn(1)])
topic_clips[1] = topic_clips[1].with_effects([vfx.CrossFadeIn(1)])
topic_clips[2] = topic_clips[2].with_effects([vfx.CrossFadeIn(1)])
topic_clips[3] = topic_clips[3].with_effects([vfx.CrossFadeIn(1)])
topic_clips[4] = topic_clips[4].with_effects([vfx.CrossFadeIn(1)])
topic_clips[5] = topic_clips[5].with_effects([vfx.CrossFadeIn(1)])
topic_clips[6] = topic_clips[6].with_effects([vfx.CrossFadeIn(1)])
topic_clips[6] = topic_clips[6].with_effects([vfx.CrossFadeIn(1)])

compo1 = CompositeVideoClip([bg_image, topic_clips[0],topic_clips[1],
                             topic_clips[2],topic_clips[3],
                             topic_clips[4],topic_clips[5],
                             topic_clips[6],topic_clips[7]])



topic_aud = AudioFileClip("topics.wav", fps=10)

topic_aud.with_start(0)

compo1.with_audio(topic_aud)

compo1.write_videofile("comp1.mp4", fps=10)