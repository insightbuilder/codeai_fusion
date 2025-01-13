from moviepy import VideoFileClip

vid_path = input("Enter your video location: ")
clip = VideoFileClip(vid_path)  # Input video
clip.write_gif("output.gif", fps=15)  # Convert to GIF
