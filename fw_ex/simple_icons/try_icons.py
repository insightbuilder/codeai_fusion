# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "simplepycons",
# ]
# ///
from simplepycons import all_icons
import os
from dotenv import load_dotenv

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
            try:
                icon = all_icons[need]
            except KeyError:
                print(f"Icon {need} not found")
                exit()
            file_svg = f"{icon_dir}{need}.svg"
            print(f"Written svg to {file_svg}")
            with open(file_svg, "w") as f:
                f.write(icon.raw_svg)
