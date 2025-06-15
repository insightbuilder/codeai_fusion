from moviepy import *
import numpy as np

# Run the code inside the movie_py
# loading the base video
video = VideoFileClip("./example_vids/async_work.mkv")

""" - agenda ⇒ 0.14 to 1.01
- dont_hire ⇒3.22 to 3.50
- communication ⇒ 7:05 to 7:25
- clear_process ⇒ 8:00 to 8:54
- open_source ⇒ 12:44 to 13:44
 """

agenda = video.subclipped(14, 61)
dont_hire = video.subclipped(202, 225)
communication = video.subclipped(425, 450)
clearproc = video.subclipped(480, 505)
opensource = video.subclipped(764, 824)

# Preview the clips

""" agenda.preview(fps=25)
dont_hire.preview(fps=25)
communication.preview(fps=25)
clearproc.preview(fps=25)
opensource.preview(fps=25) """

opensource = opensource.with_section_cut_out(start_time=50, end_time=70)

# opensource.preview(fps=25)

# Lets get some Text clips & emojis

font = "./fonts/FiraCode/FiraCodeNerdFont-Bold.ttf"
agenda_text = TextClip(font=font,
                       text="Agend is:",
                       font_size=50,
                       color="#fff")
dont_hire_text = TextClip(font=font,
                       text="Think Automation before you Hire",
                       font_size=40,
                       color="#fff")
comm_text = TextClip(font=font,
                       text="The game changer is Communication.",
                       font_size=40,
                       color="#fff")
clear_proc_text = TextClip(font=font,
                       text="Setting up Process is step towards Automation.",
                       font_size=50,
                       color="#fff")
opensource_text = TextClip(font=font,
                       text="Make it as Open Source to gain Traction.",
                       font_size=50,
                       color="#fff")

