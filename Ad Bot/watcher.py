import os
import cv2
import numpy as np
import time
import subprocess



# === Settings ===
TEMPLATE_PATHS = [
                "x_dark.png", 
                "x_light.png", 
                "ad_ready.png",
                "gold_left.png",
                "gold_right.png",
                "summon2.png",
                "x_reward_granted_light.png",
                "x_reward_granted_dark.png",
                "continue.png",
                "yes.png",
                "upgrade.png",
                "return_home.png"
                ]
ADB_PATH = "C:/Users/power/AppData/Local/Android/Sdk/platform-tools/adb.exe"
#ADB_PATH = "adb"  # Only needed if adb isn't in PATH
CONFIDENCE_THRESHOLD = 0.9
TAP_DELAY = 1.5  # Seconds between taps

def capture_screen(filename="1_screen_grab.png"):
    os.system(f"{ADB_PATH} exec-out screencap -p > {filename}")
    return cv2.imread(filename)

def find_button_location(screen, template_path):
    template = cv2.imread(template_path)
    if template is None:
        print(f"[!] Could not read template: {template_path}")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"→ {template_path} match confidence: {max_val:.3f}")
    if max_val >= CONFIDENCE_THRESHOLD:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y
    return None

def tap(x, y):
    print(f"👉 Tapping at ({x}, {y})")
    os.system(f"{ADB_PATH} shell input tap {x} {y}")
    time.sleep(TAP_DELAY)

# === Main Loop ===
def main():
    print("🚀 Starting bot loop. Press Ctrl+C to stop.")
    while True:
        screen = capture_screen()

        tapped = False
        for template in TEMPLATE_PATHS:
            coords = find_button_location(screen, template)
            if coords:
                tap(*coords)
                tapped = True
                break  # Stop after first successful tap

        if not tapped:
            print("…No 'X' found, waiting.")
            time.sleep(2)

if __name__ == "__main__":
    main()
