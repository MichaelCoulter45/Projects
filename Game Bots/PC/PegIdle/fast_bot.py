# fast_bot.py (updated)
import time
import threading
import keyboard
import sys
import os
import win32api
from collections import deque

import cv2
import numpy as np
import dxcam
import pyautogui  # fallback click

# optional win32 imports for PostMessage click (no cursor move)
try:
    import win32gui, win32con
    HAVE_WIN32 = True
except Exception:
    HAVE_WIN32 = False

# ---------------- CONFIG (tune these) ----------------
KEY_TOGGLE_BOT = "p"
KEY_MOUSE_POS = "l"
KEY_QUIT = "q"

# region to capture (left, top, width, height)
SCREEN_REGION = (0, 50, 720, 1280)
TEMPLATES_DIR = r"C:\Users\power\git\Projects\Game Bots\PC\Slime Squisher\templates\live"
MATCH_THRESHOLD = 0.75

PELLET_TRAVEL_TIME = 1   # seconds (tweak)
LEAD_MULTIPLIER = 0.8

DELAY_CLICK_MIN = 0.003     # minimal delay after a click
DELAY_LOOP_IDLE = 0.015     # when bot paused
ROI_PAD = 150               # pixels — search radius around last_x

DXCAM_FPS = 60
# ----------------------------------------------------

last_cursor_pos = None
bot_active = False
running = True
basket_history = deque(maxlen=6)
win_title = "PegIdle"

x_pos_min = 100
x_pos_max = 750
x_lead_min = -125
x_lead_max = 125


# helper: make LPARAM for client coords
def make_lparam(cx, cy):
    return (int(cy) << 16) | (int(cx) & 0xFFFF)


# global for tracking last cursor position
def click_to_game_window(win_title, screen_x, screen_y, hold_ms=6, smooth=True, move_speed=0.2):
    """
    Smoothly move cursor toward target (screen_x, screen_y) and click.
    - smooth: interpolate the cursor to avoid jitter
    - move_speed: fraction of distance to move each frame (0 < move_speed <= 1)
    """
    global last_cursor_pos
    target_x, target_y = int(screen_x), int(screen_y)
    
    # initialize last_cursor_pos
    if last_cursor_pos is None:
        last_cursor_pos = (target_x, target_y)
        
    current_x, current_y = last_cursor_pos
    
    if smooth:
        # interpolate toward target
        new_x = int(current_x + (target_x - current_x) * move_speed)
        new_y = int(current_y + (target_y - current_y) * move_speed)
    else:
        new_x, new_y = target_x, target_y
        
    last_cursor_pos = (new_x, new_y)
    
    if HAVE_WIN32 and win_title:
        hwnd = win32gui.FindWindow(None, win_title)
        if hwnd:
            try:
                x_client, y_client = win32gui.ScreenToClient(hwnd, (new_x, new_y))
                lparam = make_lparam(x_client, y_client)
                
                # move the cursor visually
                win32api.SetCursorPos((new_x, new_y))
                
                # send click messages
                win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lparam)
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
                time.sleep(hold_ms / 1000.0)
                win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
                return True
            except Exception:
                pass
            
    # fallback
    pyautogui.moveTo(new_x, new_y, duration=0.02)  # smooth fallback move
    pyautogui.click()
    return False


# ---------- load templates once (grayscale) ----------
def load_templates_gray(dir_path):
    results = []
    for fname in sorted(os.listdir(dir_path)):
        if not fname.lower().endswith(".png"):
            continue
        p = os.path.join(dir_path, fname)
        img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        h, w = img.shape[:2]
        results.append({"name": fname, "img": img, "h": h, "w": w})
    print(f"Loaded {len(results)} templates.")
    return results

def find_best_match_in_frame(gray_frame, templates, threshold=MATCH_THRESHOLD, roi=None):
    best_conf = 0.0
    best_tpl = None
    best_loc = None

    if roi is not None:
        x0, y0, x1, y1 = roi
        # clamp ROI to frame bounds
        x0 = max(0, min(x0, gray_frame.shape[1]-1))
        x1 = max(0, min(x1, gray_frame.shape[1]))
        y0 = max(0, min(y0, gray_frame.shape[0]-1))
        y1 = max(0, min(y1, gray_frame.shape[0]))
        if x1 <= x0 or y1 <= y0:
            search = gray_frame
            offset = (0, 0)
        else:
            search = gray_frame[y0:y1, x0:x1]
            offset = (x0, y0)
    else:
        search = gray_frame
        offset = (0, 0)

    # template matching loop (templates already grayscale)
    for tpl in templates:
        t = tpl["img"]
        # if template bigger than search area, skip
        if search.shape[0] < t.shape[0] or search.shape[1] < t.shape[1]:
            continue
        res = cv2.matchTemplate(search, t, cv2.TM_CCOEFF_NORMED)
        _, maxv, _, maxloc = cv2.minMaxLoc(res)
        if maxv > best_conf:
            best_conf = float(maxv)
            best_tpl = tpl
            best_loc = (int(maxloc[0] + offset[0]), int(maxloc[1] + offset[1]))

    if best_conf >= threshold:
        return best_tpl, best_conf, best_loc
    else:
        return None, best_conf, None

# optional super-fast local click using win32 mouse_event (moves cursor quickly)
def fast_click_direct(x, y):
    if HAVE_WIN32:
        win32api.SetCursorPos((int(x), int(y)))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        print("testing win32 - fast_click_direct")
    else:
        pyautogui.click(int(x), int(y))
        print("testing pyautogui - fast_click_direct")

def predict_future_x(x_current, current_fps, now=None):
    now = now or time.perf_counter()
    basket_history.append((now, x_current))
    if len(basket_history) < 2:
        return x_current, 0.0
    (t1, x1), (t2, x2) = basket_history[-2], basket_history[-1]
    dt = t2 - t1
    if dt <= 1e-6:
        return x_current, 0.0
    v_x = (x2 - x1) / dt
    frame_delay = 1.0 / max(10, current_fps)  # fallback if low
    lead_factor = (PELLET_TRAVEL_TIME + frame_delay * 2) * LEAD_MULTIPLIER
    predicted = x_current + v_x * lead_factor
    if v_x > x_lead_max:
        v_x = x_lead_max
    if v_x < x_lead_min:
        v_x = x_lead_min 
    return int(predicted), v_x

# ------------- main bot loop (dxcam) -----------------
def bot_loop(window_title=None):
    print("Bot thread ready — waiting for activation...")
    templates = load_templates_gray(TEMPLATES_DIR)
    if len(templates) == 0:
        print("No templates found — exiting.")
        return
    
    left, top, w, h = SCREEN_REGION
    cam = dxcam.create(region=(left, top, w, h), output_color="GRAY", max_buffer_len=2)
    cam.start()
    time.sleep(0.03)
    
    last_x = None
    frame_count = 0
    t_prev = time.perf_counter()
    current_fps = DXCAM_FPS
    try:
        while running:
            if not bot_active:
                time.sleep(DELAY_LOOP_IDLE)
                continue
            
            frame = cam.get_latest_frame()
            if frame is None:
                # tiny backoff if no frame
                time.sleep(0.002)
                continue
                        
            # ROI around last detection (speeds things up a lot)
            roi = None
            if last_x is not None:
                cx = int(last_x)
                x0 = max(0, cx - ROI_PAD)
                x1 = min(w, cx + ROI_PAD)
                roi = (x0, 0, x1, h)

            tpl, conf, loc = find_best_match_in_frame(frame, templates, MATCH_THRESHOLD, roi)
            v_x = 0.0
            if tpl and loc:
                x_loc, y_loc = loc
                center_x = x_loc + tpl["w"] // 2
                center_y = y_loc + tpl["h"] // 2

                predicted_x, v_x = predict_future_x(center_x, current_fps)

                # clamp predicted_x into local region (0..w-1)
                predicted_x = max(0, min(w - 1, predicted_x))

                # absolute screen coords for click
                abs_x = left + predicted_x
                abs_y = top + center_y

                # prefer PostMessage into the game window (no cursor move)
                if conf < 0.8: # Re-loops if confidence is lowwer than 80%
                    continue
                
                ok = click_to_game_window(window_title or "PegIdle", abs_x, abs_y)
                if not ok:
                    # fallback: very fast cursor click (moves cursor briefly)
                    fast_click_direct(abs_x, abs_y)
                
                last_x = center_x
                # tiny delay to avoid accidental double-clicks
                time.sleep(DELAY_CLICK_MIN)
            else:
                # clear history to avoid velocity drift on lost detections
                basket_history.clear()
                last_x = None
                # tiny idle to keep loop tight
                time.sleep(0.002)

            # perf logging every 30 frames
            frame_count += 1
            if frame_count % 30 == 0:
                now = time.perf_counter()
                current_fps = 30.0 / (now - t_prev) if (now - t_prev) > 0 else 0.0
                t_prev = now
                print(f"[perf] ~{current_fps:.1f} fps | last_conf={conf:.2f} | v_x={v_x:.1f}px/s")
    finally:
        try:
            cam.stop()
            cam.release()
        except Exception:
            pass

# -------------- hotkeys / run -----------------
def toggle_bot():
    global bot_active
    bot_active = not bot_active
    print("✅ Bot activated." if bot_active else "⏸️ Paused.")

def print_mouse_pos():
    print(pyautogui.position())

def quit_program():
    global running
    running = False
    print("🛑 Quitting...")
    sys.exit(0)

def main():
    keyboard.add_hotkey(KEY_TOGGLE_BOT, toggle_bot)
    keyboard.add_hotkey(KEY_MOUSE_POS, print_mouse_pos)
    keyboard.add_hotkey(KEY_QUIT, quit_program)

    # pass exact window title string for your Steam exe (case-sensitive)
    worker = threading.Thread(target=bot_loop, args=("Slime Squisher",), daemon=True)
    worker.start()

    print(f"""
Press [{KEY_TOGGLE_BOT.upper()}] to start/stop
Press [{KEY_MOUSE_POS.upper()}] to show mouse position
Press [{KEY_QUIT.upper()}] to quit
""")
    while running:
        time.sleep(0.1)

if __name__ == "__main__":
    main()
