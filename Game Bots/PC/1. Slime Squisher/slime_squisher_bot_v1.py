# slime_squisher_bot_v1 -> CV2, pyautogui
import cv2
import mss
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
sct = mss.mss()
hotkey_toggle_bot = 'f8' 
hotkey_exit_bot_view = 'Q'
window_name = "Slime Squisher"

bot_active = False
threshold = 0.50
cpu_cooldown = 0.00    # Max time between loops
click_delay = 0.0      # Delay between clicks

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
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    templates.append((file, img))
    return templates


templates = load_templates(TEMPLATE_DIR)
print(f"Loaded {len(templates)} templates: ")
for name, _ in templates:
    print(f"  {name}")


def run_bot(): ################################################################
    keyboard.add_hotkey(hotkey_toggle_bot, toggle_bot)
    print(f"Press {hotkey_toggle_bot.upper()} to start or stop the bot!")
    
    try:
        left, top, right, bottom = get_window_bbox(window_name)
        monitor = {"left": left, "top": top, "width": right - left, "height": bottom - top}
        print(f"Bounding window region: {left}, {top}, {right}, {bottom}")
    except Exception as e:
        print(e)
        return
    
    while True:
        if not bot_active:
            time.sleep(cpu_cooldown)
            continue
        
        # Capture only the target window region
        frame = np.array(sct.grab(monitor))
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        
        best_match = {"score": 0, "coords": None, "size": None, "name": None}
        
        # Looping over all templates
        for name, template_gray in templates:
            t_h, t_w = template_gray.shape[:2]
            result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_match["score"]:
                best_match = {"score": max_val, "coords": max_loc, "size": (t_w, t_h), "name": name}
            
        # act on only the best match
        if best_match["score"] >= threshold:
            x, y = best_match["coords"]
            t_w, t_h = best_match["size"]
            cv2.rectangle(frame, (x,y), (x + t_w, y + t_h), (0, 255, 0), 2)
            
            click_x = x + t_w // 2 + left
            click_y = y + t_h // 2 + top
            
            mouse_x, mouse_y = pyautogui.position()
            pyautogui.click(click_x, click_y)
            pyautogui.moveTo(mouse_x, mouse_y)
            print(f"Clicked {best_match["name"]} @ ({click_x}, {click_y}) - match {best_match["score"]:.2f}")
            time.sleep(click_delay)
        
        # cv2 Show what it's looking at
        # cv2.imshow("Bot Vision", frame)
        # if cv2.waitKey(1) & 0xFF == ord(hotkey_exit_bot_view):
        #     print("Exiting bot view...")
        #     break
        
        time.sleep(cpu_cooldown) # Cooldown per cycle - Helps reduce CPU use
    cv2.destroyAllWindows()


def main():
    run_bot()
if __name__ == "__main__":
    main()
