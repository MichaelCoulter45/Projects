from backend import adb_tools
from backend import matcher
import cv2
import os
import time


BASE_DIR = os.path.join(os.path.dirname(__file__))
TEMPLATE_DIR_1 = os.path.join(BASE_DIR, r"templates\games\iron_wall\ad_close")
TEMPLATE_DIR_2 = os.path.join(BASE_DIR, r"templates\games\iron_wall\ad_start")


bot_active = True
threshold = 0.90


def testing():
    print("Device size:", adb_tools.get_device_size())
    #
    img = adb_tools.get_screenshot()
    if img is not None:
        print("Screenshot shape:", img.shape)
        adb_tools.tap(500, 500)  # test tap
    else:
        print("No screenshot!")


def load_templates(*dirs):
    templates = []
    for d in dirs:
        if not os.path.isdir(d):
            print(f"Warning: {d} not found, skipping")
            continue
        for file in os.listdir(d):
            if file.endswith(".png"):
                path = os.path.join(d, file)
                templates.append((file, path))
    return templates


templates = load_templates(TEMPLATE_DIR_1, TEMPLATE_DIR_2)
print(f"Loaded {len(templates)} templates: ")
for name, path in templates:
    print(f"{name} -> {path}")


def run_bot():
    while True:
        screen = adb_tools.get_screenshot()
        adb_tools.save_screenshot()
        if screen is None:
            continue
        
        matched = False
        for name, path in templates:
            pos = matcher.match_template(screen, path, threshold)
            if pos:
                print(f"Matched {name} at {pos}, tapping...")
                adb_tools.tap(*pos)
                matched = True
                break  # one tap per cycle
            
        if not matched:
            print("No matches found.")
            
        time.sleep(1)  # cooldown per cycle






def main():
    run_bot()


if __name__ == "__main__":
    main()