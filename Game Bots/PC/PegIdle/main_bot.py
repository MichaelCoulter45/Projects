# main_bot.py
import pyautogui
import threading
import keyboard
import time
import sys
import cv2
import numpy as np
import os
from collections import deque

# Track recent basket positions for velocity estimation
basket_history = deque(maxlen=5)
PELLET_TRAVEL_TIME = 1  # seconds, tune this
LEAD_MULTIPLIER = 1.2

# --- CONFIG ---
KEY_TOGGLE_BOT = 'P'
KEY_MOUSE_POS = 'L'
KEY_QUIT = 'Q'

DELAY_KEY = 0.3
DELAY_LOOP = 0.05
DELAY_CLICK = 0.01
x_min = 100
x_max = 800

# Screenshot region (tweak for your game window)
SCREEN_REGION = (0, 50, 1920, 1030)  # (left, top, width, height)
TEMPLATES_DIR = "templates"          # folder with .png templates
MATCH_THRESHOLD = 0.75                # 0.0–1.0; adjust as needed

# --- STATE ---
bot_active = False
running = True


# --- OBJECT TEMPLATE MATCHING ---
def load_templates():
    """Load all templates from the template folder."""
    templates = []
    for f in os.listdir(TEMPLATES_DIR):
        if f.endswith(".png"):
            path = os.path.join(TEMPLATES_DIR, f)
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            if img is not None:
                templates.append((f, img))
    print(f"Loaded {len(templates)} templates from {TEMPLATES_DIR}")
    return templates


def find_best_match(frame, templates, threshold=MATCH_THRESHOLD):
    """Return best match location and confidence."""
    best_conf = 0
    best_loc = None
    best_name = None
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    for name, tmpl in templates:
        tmpl_gray = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_frame, tmpl_gray, cv2.TM_CCOEFF_NORMED)
        _, conf, _, loc = cv2.minMaxLoc(res)
        if conf > best_conf:
            best_conf = conf
            best_loc = loc
            best_name = name
            
    if best_conf >= threshold:
        return best_name, best_conf, best_loc
    else:
        return None, best_conf, None


def predict_future_x(x_current):
    """
    Predicts where the basket will be when the pellet arrives,
    based on the last few detections.
    """
    basket_history.append((time.time(), x_current))
    
    # Not enough data to calculate velocity yet
    if len(basket_history) < 2:
        return x_current, 0
    
    # Compute velocity (pixels per second)
    (t1, x1), (t2, x2) = basket_history[-2], basket_history[-1]
    dt = t2 - t1
    if dt <= 0:
        return x_current, 0
    v_x = (x2 - x1) / dt
    
    # Predict where the basket will be after travel time
    predicted_x = x_current + (v_x * PELLET_TRAVEL_TIME)
    return int(predicted_x), v_x



def match_and_click(templates):
    """Detect best match on screen and click it."""
    screenshot = pyautogui.screenshot(region=SCREEN_REGION)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    name, conf, loc = find_best_match(frame, templates)
    v_x = 0
    
    if name and loc:
        x, y = loc
        h, w = templates[0][1].shape[:2]  # assume all same size
        center_x = x + w // 2
        center_y = y + h // 2
        # --- Lead your shot ---
        predicted_x, v_x = predict_future_x(center_x)
        abs_x = SCREEN_REGION[0] + predicted_x
        abs_y = SCREEN_REGION[1] + center_y
        
        print(f"🎯 Leading shot: {center_x:.1f} → {predicted_x:.1f} | v_x={v_x:.1f}px/s")
        if abs_x <= 200 and v_x >= -200:
            abs_x = 0
        if abs_x > x_max: # No further than 800
            abs_x = x_max
        if abs_x < x_min: # No less than 100
            abs_x = x_min
        pyautogui.click(abs_x, abs_y)
        
        time.sleep(DELAY_CLICK)
    else:
        print(f"⚠️ No good match (best={conf:.2f})")
        return 0
    return v_x


# --- MAIN LOOP ---
def bot_loop():
    print("Bot thread ready — waiting for activation...")
    templates = load_templates()
    
    global bot_active
    while running:
        if bot_active:
            match_and_click(templates)
        else:
            time.sleep(DELAY_LOOP)


def toggle_bot():
    global bot_active
    bot_active = not bot_active
    print("✅ Bot activated." if bot_active else "⏸️ Pausing bot.")


def print_mouse_pos():
    print(f"Mouse position: {pyautogui.position()}")


def quit_program():
    global running
    running = False
    print("🛑 Quitting...")
    sys.exit(0)


def main():
    keyboard.add_hotkey(KEY_TOGGLE_BOT, toggle_bot)
    keyboard.add_hotkey(KEY_MOUSE_POS, print_mouse_pos)
    keyboard.add_hotkey(KEY_QUIT, quit_program)
    
    bot_thread = threading.Thread(target=bot_loop, daemon=True)
    bot_thread.start()
    
    print(f"""
Press [{KEY_TOGGLE_BOT.upper()}] to start/stop the bot
Press [{KEY_MOUSE_POS.upper()}] to show mouse position
Press [{KEY_QUIT.upper()}] to quit
""")
    
    while running:
        time.sleep(DELAY_LOOP)




if __name__ == "__main__":
    main()
