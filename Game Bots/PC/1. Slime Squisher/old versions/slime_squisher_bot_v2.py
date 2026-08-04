# slime_squisher_bot_v2 -> DXCam + match_verify integration
import cv2
import numpy as np
import os
import time
import pyautogui
import keyboard
import win32gui
import win32api
import dxcam
import concurrent.futures

from match_verify import (
    load_templates_with_orb,
    verify_and_click,
)  # <--- import from your match_verify.py

# ----------------- CONFIG ----------------- #
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR_LIVE = os.path.join(BASE_DIR, "templates", "live")
TEMPLATE_DIR_DEAD = os.path.join(BASE_DIR, "templates", "dead")
window_name = "Slime Squisher"

SCALE = 0.5  # must match match_verify.SCALE
THRESH_TEMPLATE = 0.60
structure_density = 0.02
cpu_cooldown = 0.01
click_delay = 0.01
frame_skip = 2
frame_counter = 0
bot_active = False
hotkey_toggle_bot = 'F8'
hotkey_exit_bot_view = 'Q'
# ------------------------------------------- #

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

# ----------------- Main Bot ----------------- #
def run_bot():
    global bot_active, frame_counter
    keyboard.add_hotkey(hotkey_toggle_bot, toggle_bot)
    print(f"Press {hotkey_toggle_bot.upper()} to start/stop the bot!")

    try:
        left, top, right, bottom = get_window_bbox(window_name)
        width, height = right - left, bottom - top

        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        left = max(0, left)
        top = max(50, top)
        width = min(width, screen_width - left)
        height = min(height, screen_height - top)

        monitor_region = {"left": left, "top": top, "width": width, "height": height}
        print(f"Monitoring window region: {monitor_region}")
    except Exception as e:
        print(e)
        return

    # Initialize DXCamera
    cam = dxcam.create(region=(left, top, width, height))
    time.sleep(0.2)
    cam.start()

    # ---------------- Load templates ---------------- #
    print("Loading live slime templates...")
    live_templates = load_templates_with_orb(TEMPLATE_DIR_LIVE, scale=SCALE)
    print(f"Loaded {len(live_templates)} live templates.")
    print("Loading puddle (dead slime) templates...")
    dead_templates = []
    if os.path.exists(TEMPLATE_DIR_DEAD):
        dead_templates = load_templates_with_orb(TEMPLATE_DIR_DEAD, scale=SCALE)
    print(f"Loaded {len(dead_templates)} dead templates.")
    
    print(f"Press {hotkey_toggle_bot.upper()} to start/stop the bot!")
    print("Bot ready — waiting for activation.")
    # ------------------------------------------------ #

    while True:
        if not bot_active:
            time.sleep(0.1)
            continue
        key = cv2.waitKey(1) & 0xFF

        frame = cam.get_latest_frame()
        if frame is None:
            continue

        frame_counter += 1
        if frame_counter % frame_skip != 0:
            continue

        # Downscale frame
        frame_small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)
        frame_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)

        # ---------- Fast pass: best template by correlation ----------
        best_score = -1
        best_template = None
        best_loc = None

        for tpl in live_templates:
            res = cv2.matchTemplate(frame_gray, tpl["img_small"], cv2.TM_CCOEFF_NORMED)
            _, mv, _, ml = cv2.minMaxLoc(res)
            if mv > best_score:
                best_score = mv
                best_template = tpl
                best_loc = ml

        if best_template is None:
            continue
        
        # ---------- Verify the match ----------
        # Compute edge density around the matched area
        x, y = best_loc
        h, w = best_template["img"].shape[:2]
        roi = frame_gray[
            max(0, y - 4):min(frame_gray.shape[0], y + h + 4),
            max(0, x - 4):min(frame_gray.shape[1], x + w + 4)
        ]
        
        edges = cv2.Canny(roi, 50, 150)
        edge_density = cv2.countNonZero(edges) / float(edges.size)
        
        # Adaptive threshold logic (so we don't get stuck at high values)
        adaptive_threshold = max(THRESH_TEMPLATE, min(0.95, best_score - 0.12))
        is_structured = edge_density > 0.015
        
        # Override for very high scores (force click)
        force_click = best_score >= 0.93
        
        # Logging for insight
        print(f"DEBUG threshold={adaptive_threshold:.2f} | force={force_click} | edges={edge_density:.3f}")
        
        if force_click or best_score >= adaptive_threshold or (is_structured and best_score >= adaptive_threshold - 0.05):
            verified = verify_and_click(
                frame_full_bgr=frame,
                frame_resized_gray=frame_gray,
                best_template=best_template,
                best_loc=best_loc,
                left=left,
                top=top,
                scale=SCALE,
                negative_templates=dead_templates,
                force_click=force_click,
            )
            if verified:
                print(f"✅ Clicked live slime [{best_template['name']}] | score={best_score:.2f} | edges={edge_density:.3f}")
                time.sleep(click_delay)
            else:
                print(f"❌ Rejected [{best_template['name']}] | score={best_score:.2f} | failed verification | edges={edge_density:.3f}")
        else:
            reason = "low structure" if not is_structured else "below adaptive threshold"
            print(f"❌ Rejected [{best_template['name']}] | score={best_score:.2f} | {reason} | edges={edge_density:.3f}")
            
            
        # ---------- Debug Vision ----------
        cv2.imshow("Bot Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord(hotkey_exit_bot_view):
            print("Exiting bot view...")
            break
        
        time.sleep(cpu_cooldown)
        if key == ord('q'):
            print("Exiting bot...")
            break

# ----------------- Run ----------------- #
if __name__ == "__main__":
    run_bot()
