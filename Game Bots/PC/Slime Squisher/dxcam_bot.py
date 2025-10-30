import cv2
import numpy as np
import os
import time
import pyautogui
import keyboard
import win32gui
import win32api
import dxcam  # pip install dxcam
import concurrent.futures

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
window_name = "Slime Squisher"
scale = 0.5
frame_skip = 2
frame_counter = 0

bot_active = False
threshold = 0.50
cpu_cooldown = 0.005
click_delay = 0.01
hotkey_toggle_bot = 'F8'
hotkey_exit_bot_view = 'Q'

# ----------------- Functions ----------------- #
def toggle_bot():
    global bot_active
    bot_active = not bot_active
    print(f"Bot {'activated' if bot_active else 'paused'}")

def get_window_bbox(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return left, top, right, bottom
    else:
        raise Exception(f"Window '{window_name}' not found!")

def load_templates(template_dir):
    templates = []
    for file in os.listdir(template_dir):
        path = os.path.join(template_dir, file)
        if os.path.isfile(path):
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                templates.append((file, img))
    return templates

# ----------------- Load ----------------- #
templates = load_templates(TEMPLATE_DIR)
print(f"Loaded {len(templates)} templates:")
for name, _ in templates:
    print(" ", name)

# ----------------- Main Bot ----------------- #
def run_bot():
    global bot_active
    keyboard.add_hotkey(hotkey_toggle_bot, toggle_bot)
    print(f"Press {hotkey_toggle_bot.upper()} to start/stop the bot!")

    try:
        left, top, right, bottom = get_window_bbox(window_name)
        width, height = right - left, bottom - top

        # Clip to monitor bounds
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        left = max(0, left)
        top = max(100, top)
        width = min(width, screen_width - left)
        height = min(height, screen_height - top)

        monitor_region = {"left": left, "top": top, "width": width, "height": height}
        print(f"Monitoring window region: {monitor_region}")
    except Exception as e:
        print(e)
        return

    # Initialize DXCamera
    cam = dxcam.create(region=(left, top, width, height))
    time.sleep(0.2)  # give camera a moment to start
    cam.start()
    
    # Load templates once
    templates = load_templates(TEMPLATE_DIR)
    print(f"Loaded {len(templates)} templates:")
    for name, _ in templates:
        print(" ", name)
    
    while True:
        if not bot_active:
            time.sleep(0.1)
            continue
        key = cv2.waitKey(1) & 0xFF # Idk it helps with shutting the program down with Ctrl+C
        
        frame = cam.get_latest_frame()
        if frame is None:
            continue
        
        frame_counter += 1
        if frame_counter % frame_skip != 0:
            continue
        
        # Downscale frame
        frame_small = cv2.resize(frame, (0,0), fx = scale, fy = scale)
        frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
        
        best_match = {"score": 0, "coords": None, "size": None, "name": None}
        
        # Threaded template matching
        def match_one(template_tuple):
            name, template = template_tuple
            t_h, t_w = template.shape[:2]
            template_resized = cv2.resize(template, (int(t_w * scale), int(t_h * scale)))
            result = cv2.matchTemplate(frame_gray, template_resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            return name, max_val, max_loc, (t_w, t_h)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(match_one, templates))
        
        # Loop over all templates and find the best single match
        for name, max_val, max_loc, (t_w, t_h) in results:
            if max_val > best_match["score"]:
                best_match = {"score": max_val, "coords": max_loc, "size": (t_w, t_h), "name": name}
                
        # Click best match
        if best_match["score"] >= threshold:
            x, y = best_match["coords"]
            t_w, t_h = best_match["size"]
            cv2.rectangle(frame, (x, y), (x + t_w, y + t_h), (0, 0, 255), 2)
            
            x = int(x / scale)
            y = int(y / scale)
            click_x = x + t_w // 2 + left
            click_y = y + t_h // 2 + top
            
            mouse_x, mouse_y = pyautogui.position()
            pyautogui.click(click_x, click_y)
            pyautogui.moveTo(mouse_x, mouse_y)
            
            print(f"Clicked {best_match['name']} @ ({click_x}, {click_y}) - score {best_match['score']:.2f}")
            time.sleep(click_delay)
        else:
            print("No template matched above threshold.")
        
        # Show debug vision
        cv2.imshow("Bot Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord(hotkey_exit_bot_view):
            print("Exiting bot view...")
            break
        
        time.sleep(cpu_cooldown)
        # Exit helper
        if key == ord('q'):
            print("Exiting template capture helper...")
            break
# ----------------- Run ----------------- #
if __name__ == "__main__":
    run_bot()