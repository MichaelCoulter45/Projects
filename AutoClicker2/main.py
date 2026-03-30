import win32api, win32gui, win32con
import threading
import keyboard
import ctypes
import time
import random
import gui


bot_running = True
active = False
max_cps = 250

########################################################
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]
########################################################
def click():
    extra = ctypes.c_ulong(0)
    
    down = INPUT(type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra)))
    
    up = INPUT(type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra)))
    
    ctypes.windll.user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
    time.sleep(random.uniform(0.045, 0.065))
    ctypes.windll.user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))


def start_bot():
    global hwnd
    window_name = gui.window_entry.get()
    
    if not window_name:
        gui.status_label.config(text="ENTER WINDOW NAME", fg="orange")
        return
    
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        gui.status_label.config(text="WINDOW NOT FOUND", fg="red")
        return
    
    gui.status_label.config(text="READY", fg="blue")
    keyboard.add_hotkey(gui.keybind_toggle, toggle_bot)
    
    threading.Thread(target=auto_clicker, daemon=True).start()


def toggle_bot():
    global active
    active = not active
    if active:
        print(f"✅ Bot Activated!")
        gui.status_label.config(text="✅ RUNNING", fg="green")
    else:
        print(f"⏸️ Pausing...")
        gui.status_label.config(text="⏸️ PAUSED", fg="blue")
########################################################
def auto_clicker():
    """ This works even when the target window isn't in focus.
    Thanks to win32gui.PostMessage(...)!"""
    global bot_running, active
    
    counter = 0
    lparam = win32api.MAKELONG(500,500)
    # start = time.perf_counter()
    
    while bot_running:
        if not active:
            time.sleep(0.05)
            continue
        
        cps = get_cps()
        if cps is None:
            time.sleep(0.05)
            continue
        
        cps = min(cps, max_cps) # This limits the cps to MAX_CPS to prevent outragous numbers and accidentally locking the cpu.
        delay = max(0.001, 1/cps) # Never below 1ms
        
        click()
        time.sleep(delay)
    #     # counter += 1
    # end = time.perf_counter()
    # print(f"Done! Calculated CPS: {counter / (end-start):.2f}")


def get_cps():
    try:
        cps = float(gui.cps_entry.get())
        if cps <= 0:
            raise ValueError
        return cps
    except ValueError:
        gui.status_label.config(text="INVALID CPS", fg="red")
        return None














