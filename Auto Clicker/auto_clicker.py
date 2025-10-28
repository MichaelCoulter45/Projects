import tkinter as tk
import threading
import pyautogui
import time
import keyboard
# BASH: pyinstaller --noconfirm --clean --onefile auto_clicker.py

clicking = False
hotkey_start = 'S'
hotkey_stop = 'Q'

def start_clicking():
    global clicking
    if clicking:
        return
    clicking = True
    status_label.config(text="Status: RUNNING", fg="green")
    threading.Thread(target=click_loop, daemon=True).start()


def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Status: STOPPED", fg="red")


def click_loop():
    delay = float(delay_entry.get())
    duration = float(duration_entry.get())
    start_time = time.time()
    
    while clicking and (time.time() - start_time < duration):
        pyautogui.click()
        time.sleep(delay)
        
    stop_clicking()


def listen_hotkeys():
    keyboard.add_hotkey(hotkey_start, start_clicking)
    keyboard.add_hotkey(hotkey_stop, stop_clicking)
    keyboard.wait()  # keeps listening in background

# GUI setup
root = tk.Tk()
root.title("Simple Auto Clicker")

tk.Label(root, text="Click Delay (sec):").grid(row=0, column=0, padx=5, pady=5)
delay_entry = tk.Entry(root)
delay_entry.insert(0, "0.001")
delay_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Duration (sec):").grid(row=1, column=0, padx=5, pady=5)
duration_entry = tk.Entry(root)
duration_entry.insert(0, "600")
duration_entry.grid(row=1, column=1, padx=5, pady=5)

start_button = tk.Button(root, text="Start", command=start_clicking)
start_button.grid(row=2, column=0, padx=5, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_clicking)
stop_button.grid(row=2, column=1, padx=5, pady=10)

tk.Label(root, text=f"Start = {hotkey_start}").grid(row=3, column=0, padx=5, pady=5)
duration_entry = tk.Entry(root)
duration_entry.insert(0, "5")
duration_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text=f"Stop = {hotkey_stop}").grid(row=3, column=1, padx=5, pady=5)
duration_entry = tk.Entry(root)
duration_entry.insert(0, "5")
duration_entry.grid(row=1, column=1, padx=5, pady=5)

status_label = tk.Label(root, text="Status: STOPPED", fg="red")
status_label.grid(row=4, column=0, columnspan=2, pady=5)

threading.Thread(target=listen_hotkeys, daemon=True).start()

root.mainloop()
