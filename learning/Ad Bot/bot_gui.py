import os
import cv2
import numpy as np
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

ADB_PATH = "C:/Users/power/AppData/Local/Android/Sdk/platform-tools/adb.exe"
CONFIDENCE_THRESHOLD = 0.9
TAP_DELAY = 1.5
TEMPLATE_PATHS = [
    "x_dark.png", "x_light.png", "ad_ready.png", "gold_left.png",
    "gold_right.png", "summon2.png", "x_reward_granted_light.png",
    "x_reward_granted_dark.png", "continue.png", "yes.png",
    "upgrade.png", "return_home.png"
]

class BotApp:
#######
    def __init__(self, root):
        self.root = root
        self.root.title("Android Bot GUI")
        self.running = False
        
        self.start_button = tk.Button(root, text="Start Bot", command=self.start_bot)
        self.stop_button = tk.Button(root, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.log = scrolledtext.ScrolledText(root, width=60, height=20, state=tk.DISABLED)
        
        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.log.pack(padx=10, pady=10)
#######
    def log_message(self, message):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)
#######
    def start_bot(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log_message("🚀 Bot started.")
        threading.Thread(target=self.run_bot, daemon=True).start()
#######
    def stop_bot(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("🛑 Bot stopped.")
#######
    def run_bot(self):
        while self.running:
            screen = self.capture_screen()
            tapped = False
            for template in TEMPLATE_PATHS:
                coords = self.find_button_location(screen, template)
                if coords:
                    self.tap(*coords)
                    self.log_message(f"👉 Tapped: {template} at {coords}")
                    tapped = True
                    break
                else:
                    self.log_message(f"…No match for {template}")
                    
            if not tapped:
                time.sleep(2)
#######
    def capture_screen(self, filename="screen.png"):
        os.system(f"{ADB_PATH} exec-out screencap -p > {filename}")
        return cv2.imread(filename)
#######
    def find_button_location(self, screen, template_path):
        template = cv2.imread(template_path)
        if template is None:
            self.log_message(f"[!] Could not load {template_path}")
            return None
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= CONFIDENCE_THRESHOLD:
            h, w = template.shape[:2]
            return (max_loc[0] + w // 2, max_loc[1] + h // 2)
        return None
#######
    def tap(self, x, y):
        os.system(f"{ADB_PATH} shell input tap {x} {y}")
        time.sleep(TAP_DELAY)

if __name__ == "__main__":
    root = tk.Tk()
    app = BotApp(root)
    root.mainloop()
