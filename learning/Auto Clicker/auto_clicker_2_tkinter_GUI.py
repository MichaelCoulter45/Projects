import win32gui, win32api, win32con
import ctypes
import tkinter as tk
from tkinter import ttk
import keyboard
import time
import threading


""" 
This app has a GUI and asks for a window title you are targeting.
The default clicks per second is set to 500 though it may
never get to that actual speed.
After typing your desired window title, click start and the program
will look for a window with that title. If it finds it, then you can
hit the hotkey " . " to toggle the bot on and off.
If it doesn't find the window title then it asks you to try again.
"""
# Keybinds
keybind_toggle = '.'


# Bot Stuff
bot_running = True
active = False
delay_cpu = 0.1
MAX_CPS = 250



# Pre-define constants for speed
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
MK_LBUTTON = 0x0001

#############   Functions   ############
def start_bot():
    global hwnd
    window_name = window_entry.get()
    
    if not window_name:
        status_label.config(text="ENTER WINDOW NAME", fg="orange")
        return
    
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        status_label.config(text="WINDOW NOT FOUND", fg="red")
        return
    
    status_label.config(text="READY", fg="blue")
    keyboard.add_hotkey(keybind_toggle, toggle_bot)
    
    threading.Thread(target=auto_clicker, daemon=True).start()


def toggle_bot():
    global active
    active = not active
    if active:
        print(f"✅ Bot Activated!")
        status_label.config(text="✅ RUNNING", fg="green")
    else:
        print(f"⏸️ Pausing...")
        status_label.config(text="⏸️ PAUSED", fg="blue")


def auto_clicker():
    """ This works even when the target window isn't in focus.
    Thanks to win32gui.PostMessage(...)!"""
    global bot_running, active
    click_event = ctypes.windll.user32.mouse_event
    
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
        
        cps = min(cps, MAX_CPS) # This limits the cps to MAX_CPS to prevent outragous numbers and accidentally locking the cpu.
        delay = max(0.001, 1/cps) # Never below 1ms
        
        click_event(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lparam)
        time.sleep(delay)
        click_event(hwnd, WM_LBUTTONUP, 0, lparam)
    #     # counter += 1
    # end = time.perf_counter()
    # print(f"Done! Calculated CPS: {counter / (end-start):.2f}")


def get_cps():
    try:
        cps = float(cps_entry.get())
        if cps <= 0:
            raise ValueError
        return cps
    except ValueError:
        status_label.config(text="INVALID CPS", fg="red")
        return None









###### GUI SETUP
root = tk.Tk()
root.title("Michael's Auto Clicker")

tk.Label(root, text="Game Window:").grid(row=0, column=0, padx=5, pady=5)
window_entry = tk.Entry(root)
window_entry.insert(0,"Window Name")
window_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Clicks Per Second:").grid(row=1, column=0, padx=5, pady=5)
cps_entry = tk.Entry(root)
cps_entry.insert(0,"60")
cps_entry.grid(row=1, column=1, padx=5, pady=10)

tk.Label(root, text=f"Toggle Hotkey: [ {keybind_toggle} ]").grid(row=2, column=0, padx=5, pady=5)

status_label = tk.Label(root, text="ENTER WINDOW NAME", fg="orange")
status_label.grid(row=3, column=0, columnspan=2, pady=5)


start_button = ttk.Button(root, text="✅ Start", command=start_bot)
start_button.grid(row=4, column=0, padx=5, pady=5)

quit_button = ttk.Button(root, text="🚫 Quit", command=root.destroy)
quit_button.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()



###########
# def main():
    # keyboard.add_hotkey(keybind_toggle, toggle_bot)
    # auto_clicker(hwnd, 250, 250)
# if __name__ == "__main__":
    # main()