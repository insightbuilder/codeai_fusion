from moviepy import * # type: ignore
import numpy as np

# Run the code inside the movie_py
# loading the base video
video = VideoFileClip("./example_vids/async_work.mkv")

""" 
These were changed after first run
- agenda ⇒ 0.14 to 0.30
- dont_hire ⇒3.22 to 3.50
- communication ⇒ 7:05 to 7:25
- clear_process ⇒ 8:00 to 8:54
- open_source ⇒ 12:44 to 13:44
"""

agenda = video.subclipped(14, 30)
dont_hire = video.subclipped(202, 225)
communication = video.subclipped(425, 450)
clearproc = video.subclipped(480, 505)
opensource = video.subclipped(764, 790)

print(dir(agenda))
# Preview the clips

""" agenda.preview(fps=25)
dont_hire.preview(fps=25)
communication.preview(fps=25)
clearproc.preview(fps=25)
opensource.preview(fps=25) """

opensource = opensource.with_section_cut_out(start_time=10, end_time=15)

# opensource.preview(fps=25)

# Lets get some Text clips & emojis

font = "./fonts/FiraCode/FiraCodeNerdFont-Bold.ttf"
agenda_text = TextClip(font=font,
                       text="Agend is:",
                       font_size=50,
                       color="#000")
agenda_text = agenda_text.with_position(("center", 200))
dont_hire_text = TextClip(font=font,
                       text="Think Automation before you Hire",
                       font_size=40,
                       color="#000")
dont_hire_text = dont_hire_text.with_position(("center", 200))
comm_text = TextClip(font=font,
                       text="The game changer is Communication.",
                       font_size=40,
                       color="#000")
comm_text = comm_text.with_position(("center", 200))
clear_proc_text = TextClip(font=font,
                       text="Setting up Process is step towards Automation.",
                       font_size=50,
                       color="#000")
clear_proc_text = clear_proc_text.with_position(("center", 200))
opensource_text = TextClip(font=font,
                       text="Make it as Open Source to gain Traction.",
                       font_size=50,
                       color="#000")
opensource_text.with_position(("center", 200))

## Adding logo clips
aa = ImageClip(img="./example_vids/1F4AA.png")
p4a = ImageClip(img="./example_vids/1F44A.png")
p4c = ImageClip(img="./example_vids/1F44C.png")
p4d = ImageClip(img="./example_vids/1F44D.png")


## Adding the duration for the text clips

agenda_text = agenda_text.with_duration(8).with_start(5)
aa = aa.with_start(agenda.start + 2).with_end(agenda_text.end)

dont_hire = dont_hire.with_start(agenda.end)
dont_hire_text = dont_hire_text.with_start(dont_hire.start + 2).with_end(dont_hire.start + 10)
p4a = p4a.with_start(dont_hire_text.start + 1).with_end(dont_hire_text.end)

communication = communication.with_start(dont_hire.end)
comm_text = comm_text.with_start(communication.start+2).with_end(communication.end-10)
p4c = p4c.with_start(communication.start + 4).with_duration(5)

clearproc = clearproc.with_start(communication.end)
clear_proc_text = clear_proc_text.with_duration(5).with_start(clearproc.start + 2)

opensource = opensource.with_start(clearproc.end)
opensource_text  = opensource_text.with_duration(5).with_start(opensource.start + 2)
p4d = p4d.with_start(opensource_text.start + 5).with_duration(5)

### First Compo

first_compo = CompositeVideoClip([
    agenda, agenda_text, aa, dont_hire, dont_hire_text, p4a,
    communication, comm_text, p4c,
    clearproc, clear_proc_text, opensource, opensource_text, 
    p4d
])

# first_compo.preview(fps=25)

agenda = agenda.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])
dont_hire = dont_hire.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])
communication = communication.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])
clearproc = clearproc.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])
opensource = opensource.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])

agenda_text = agenda_text.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
dont_hire_text = dont_hire_text.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
comm_text = comm_text.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
clear_proc_text = clear_proc_text.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
opensource_text = opensource_text.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])

second_compo = CompositeVideoClip([
    agenda, agenda_text, aa, dont_hire, dont_hire_text, p4a,
    communication, comm_text, p4c,
    clearproc, clear_proc_text, opensource, opensource_text, 
    p4d
])

# second_compo.preview(fps=25)

second_compo.write_videofile("./results/auto_edit.mp4")