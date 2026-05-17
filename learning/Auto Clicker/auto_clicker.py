import tkinter as tk
import threading
import time
import keyboard
import win32api, win32con

# Global state
clicking = False
hotkey_toggle_bot = '.'

# ---------------- FAST CLICK FUNCTION ----------------
def fast_click_loop():
    """High-speed click loop using Win32 API."""
    global clicking
    try:
        cps = float(cps_entry.get())
        cps = max(1, min(cps, 2000))  # Clamp 1–2000 CPS
    except ValueError:
        cps = 10

    delay = 1.0 / cps
    click_count = 0
    start_time = time.time()

    while clicking:
        # Perform left click
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        click_count += 1

        # Print every second
        now = time.time()
        if now - start_time >= 1:
            real_cps = click_count / (now - start_time)
            print(f"Actual CPS: {real_cps:.1f}")
            click_count = 0
            start_time = now

        # Wait until next click
        time.sleep(delay)

    stop_clicking()

# ---------------- CONTROL FUNCTIONS ----------------
def toggle_clicking():
    """Toggle auto-clicker on/off."""
    global clicking
    if clicking:
        stop_clicking()
    else:
        start_clicking()

def start_clicking():
    global clicking
    clicking = True
    status_label.config(text="Status: RUNNING", fg="green")
    threading.Thread(target=fast_click_loop, daemon=True).start()

def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Status: STOPPED", fg="red")

def listen_hotkeys():
    keyboard.add_hotkey(hotkey_toggle_bot, toggle_clicking)
    keyboard.wait()

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Fast Auto Clicker")

tk.Label(root, text="Clicks per Second:").grid(row=0, column=0, padx=5, pady=5)
cps_entry = tk.Entry(root)
cps_entry.insert(0, "2500")  # Default CPS
cps_entry.grid(row=0, column=1, padx=5, pady=5)

start_button = tk.Button(root, text="Start", command=start_clicking)
start_button.grid(row=1, column=0, padx=5, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_clicking)
stop_button.grid(row=1, column=1, padx=5, pady=10)

tk.Label(root, text=f"Toggle Hotkey = {hotkey_toggle_bot}").grid(row=2, column=0, columnspan=2)
status_label = tk.Label(root, text="Status: STOPPED", fg="red")
status_label.grid(row=3, column=0, columnspan=2, pady=5)

threading.Thread(target=listen_hotkeys, daemon=True).start()

root.mainloop()
