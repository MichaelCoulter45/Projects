import win32api, win32gui, win32con
import threading
import tkinter as tk
from tkinter import ttk
import keyboard
import time
import dxcam, cv2
import pyautogui
import easyocr
import numpy as np


# 1. Needs a typing bot
# 2. Needs a screen reading bot to know what to type
# 3. ----- Implement a GUI to make it interesting and new user friendly.
# 4. Shave the capture area to reduce cpu load and time
# 5. Have the screen reader stop and execute once it finds any match. --> increasing speed

# Keybinds
keybind_toggle = '.'


# Bot Stuff
bot_running = True
bot_active = False
delay_cpu = 0.5



################# Functions #################
def start_bot():
    window_name = window_entry.get()
    
    if not window_name:
        status_label.config(text="ENTER WINDOW TITLE", fg="orange")
        return
    
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        status_label.config(text="WINDOW NOT FOUND", fg="red")
        return
    
    status_label.config(text="READY", fg="blue")
    keyboard.add_hotkey(keybind_toggle, toggle_bot)
    threading.Thread(target=typer_bot, daemon=True).start()


def toggle_bot():
    global bot_active
    bot_active = not bot_active
    if bot_active:
        print(f"✅ Bot Activated!")
        status_label.config(text="✅ RUNNING", fg="green")
    else:
        print(f"⏸️ Pausing...")
        status_label.config(text="⏸️ PAUSED", fg="blue")


def typer_bot():
    window_name = window_entry.get()
    hwnd = win32gui.FindWindow(None, window_name)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    crop_region = (
        left + int(width* 0.1),
        top + int(height * 0.2),
        right - int(width * 0.1),
        bottom - int(height * 0.1)
    )
    # Camera Capture
    camera = dxcam.create()
    reader = easyocr.Reader(['en'], gpu=False) # No dedicated GPU..
    camera.start(region=(crop_region),target_fps=15)
    history = {}
    
    while True:
        if bot_active:
            current_time = time.time()
            frame = camera.get_latest_frame()
            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                _, binary_frame = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
                # OCR on the latest frame
                results = reader.readtext(
                    binary_frame,
                    detail=0,
                    paragraph=False,
                    contrast_ths=0.1,
                    adjust_contrast=0.0
                    )
                # Debugging  View
                cv2.imshow("Debug View", binary_frame)
                cv2.waitKey(1)
                
                for word in results:
                    word = word.lower().strip()
                    if word not in history:
                        print(f"Printing: {word}")
                        pyautogui.write(word)
                        pyautogui.press("delete")
                        history[word] = current_time
                history = {w: t for w, t in history.items() if current_time - t < 3}
        else:
            time.sleep(delay_cpu)






################### GUI ###################
root = tk.Tk()
root.title("Michael's Type Knight Bot")

tk.Label(root, text="Game Window:").grid(row=0,column=0,padx=5,pady=5)
window_entry = tk.Entry(root)
window_entry.insert(0, "Type Knight")
window_entry.grid(row=0,column=1,padx=5,pady=5)

tk.Label(root, text=f"Toggle Key: [ {keybind_toggle} ]").grid(row=2,column=0,padx=5,pady=5)

status_label = tk.Label(root,text="ENTER WINDOW TITLE", fg="orange")
status_label.grid(row=3,column=0,padx=5,pady=5)

start_button = ttk.Button(root, text=" ✅ Start ", command=start_bot)
start_button.grid(row=4,column=0,padx=5,pady=5)

quit_button = ttk.Button(root, text=" 🚫 Quit ", command=root.destroy)
quit_button.grid(row=4,column=1,padx=5,pady=5)

root.mainloop()
####################################
# def main():

# if __name__ == "__main__":
#     main()