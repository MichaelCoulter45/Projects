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

######
def capture_screen():
    result = subprocess.run (
        [ADB_PATH, "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE
    )
    image_bytes = result.stdout
    image_array = np.frombuffer(image_bytes, np.uint8)
    screen = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return screen
######
def find_button_location(screen, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"[!] Could not read template: {template_path}")
        return None
    
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    print(f"→ {template_path} match confidence: {max_val:.3f}")
    if max_val >= CONFIDENCE_THRESHOLD:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y
    return None
######
def tap(x, y):
    print(f"👉 Tapping at ({x}, {y})")
    os.system(f"{ADB_PATH} shell input tap {x} {y}")
    time.sleep(TAP_DELAY)
######
def screens_are_similar(img1, img2, threshold=0.99):
    if img1 is None or img2 is None:
        return False
    if img1.shape != img2.shape:
        return False
    diff = cv2.absdiff(img1, img2)
    non_zero = np.count_nonzero(diff)
    total_pixels = np.prod(img1.shape)
    similarity = 1 - (non_zero / total_pixels)
    return similarity >= threshold

# === Main Loop === #
def main():
    print("🚀 Starting bot loop. Press Ctrl+C to stop.")
    prev_screen = None
    while True:
        screen = capture_screen()   
        
        if screens_are_similar(screen, prev_screen):
            print("...Screen hasn't changed, skipping.")
            time.sleep(1)
            continue
        
        prev_screen = screen
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
