from moviepy import VideoFileClip
import tkinter as tk
from tkinter import filedialog

# Open file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window
file_path = filedialog.askopenfilename(
    title="Select a Video File", filetypes=[("MP4 files", "*.mp4")]
)

if file_path:  # If a file is selected
    output_path = file_path.rsplit(".", 1)[0] + ".gif"  # Save as .gif in same location
    clip = VideoFileClip(file_path)
    clip.write_gif(output_path, fps=15)
    print(f"GIF saved at: {output_path}")
else:
    print("No file selected!")
