# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "simpleicons[imaging]",
#     "simplepycons",
# ]
# ///
from simpleicons.all import icons
from simpleicons.image import icon_to_image

import os
from dotenv import load_dotenv
from PIL import Image

# Increase Pillow’s safety limit
Image.MAX_IMAGE_PIXELS = None

load_dotenv()

# check if the input is empty
while True:
    need = input("Which Brand Icon are you looking for: ")
    if need == "":
        print("Please enter an icon / brand name")
    # check if the input is "exit"
    elif need == "exit":
        print("Goodbye")
        exit()
    else:
        # check if the input is in the list of icons
        icon_dir = os.environ["ICON_DIR"]
        icons_in_dir = os.listdir(icon_dir)
        for icon in icons_in_dir:
            if need in icon:
                print(f"Found {icon}")
        user_satisfied = input("Are there the icons you want: ?")
        # check if the user is satisfied
        if user_satisfied == "y":
            print("Have a great day..")
            exit()
        # inform user that we will try to fetch the icons
        else:
            print("Lets try to fetch the icons")
            size = 75
            try:
                icon = icons.get(need)
            except KeyError:
                print(f"Icon {need} not found")
                exit()
            xml_bytes = icon.get_xml_bytes(fill="orange")
            img = icon_to_image(xml_bytes, bg=None, scale=(size, size))
            # img = img.resize((size, size), Image.LANCZOS)
            img = img.convert("RGBA")
            # img.putalpha(255)
            file_png = f"{icon_dir}{need}.png"
            print(f"Written png to {file_png}")
            img.save(file_png, format="PNG")
