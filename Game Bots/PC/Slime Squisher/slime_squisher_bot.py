import cv2
import numpy as np
import os
import time
import pyautogui
import keyboard
import win32gui


"""
Goals for this program:
- Auto Click slimes
- target the same slime until dead
- target slimes based on how close they are to strawberry
- Add in keyboard hotkeys
- Add at least a simple GUI
- Start / Stop with keyboard keys, audio cues, visual cues
- Add region bounding
- Add visual feedback by drawing rectangles with cv2.rectangle
- Make a single file exe to run program outside of VSCode

"""

BASE_DIR = os.path.join(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, r"templates")

bot_active = False
threshold = 0.45
cpu_cooldown = 0.1
click_delay = 0.1
hotkey_toggle_bot = 'f8' 
window_name = "Slime Squisher"


def get_window_bbox(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        # rect = (left, top, right, bottom)
        return rect
    else:
        raise Exception(f"Window '{window_name} not found!")


def toggle_bot():
    global bot_active
    bot_active = not bot_active
    print(f"Bot {'activated' if bot_active else 'paused'}")


def load_templates(*dirs):
    templates = []
    for d in dirs:
        if not os.path.isdir(d):
            print(f"Warning: {d} not found. Skipping.")
            continue
        for file in os.listdir(d):
            path = os.path.join(d, file)
            if os.path.isfile(path):
                templates.append((file, path))
    return templates


templates = load_templates(TEMPLATE_DIR)
print(f"Loaded {len(templates)} templates: ")
for name, path in templates:
    print(f"  {name} -> {path}")


def run_bot():
    keyboard.add_hotkey(hotkey_toggle_bot, toggle_bot)
    print(f"Press {hotkey_toggle_bot.upper()} to start or stop the bot!")
    
    try:
        left, top, right, bottom = get_window_bbox(window_name)
        print(f"Bounding window region: {left}, {top}, {right}, {bottom}")
    except Exception as e:
        print(e)
        return
    
    while True:
        if not bot_active:
            time.sleep(0.1)
            continue
        # Capture only the target window region
        screen = pyautogui.screenshot(region=(left, top, right - left, bottom - top))
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        for name, path in templates:
            img_template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img_template is None:
                continue
            
            # Convert to Gray for more stable detection
            template_gray = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY)
            t_h, t_w = img_template.shape[:2]
        
        # Find Matches
        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        
        # For every match, click the center
        for pt in zip(*loc[::-1]):
            x, y = pt[0] + t_w // 2 + left, pt[1] + t_h // 2 + top # adjusting coords to screen reigon
            pyautogui.click(x, y)
            time.sleep(click_delay)
        
        time.sleep(cpu_cooldown) # Cooldown per cycle - Helps reduce CPU use






def main():
    run_bot()
if __name__ == "__main__":
    main()