import os
import time
import cv2
import numpy as np
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import ttk, filedialog, simpledialog, messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import subprocess

ADB_PATH = "C:/Users/power/AppData/Local/Android/Sdk/platform-tools/adb.exe"
TEMPLATE_PATHS = [
    "x_dark.png",
    "x_light.png",
    "ad_ready.png",
    "gold_left.png",
    "gold_right.png",
    "summon2.png",
    "x_reward_granted_light.png",
    "x_reward_granted_dark.png",
    "continue.png",
    "yes.png",
    "upgrade.png",
    "return_home.png"
]

CONFIDENCE_THRESHOLD = 0.9
TAP_DELAY = 1.5

class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Bot Controller")

        self.template_vars = {}
        self.running = False

        # Checkbox section
        self.checkbox_frame = ttk.LabelFrame(root, text="Select Buttons to Tap")
        self.checkbox_frame.pack(padx=10, pady=10, fill="x")

        for path in TEMPLATE_PATHS:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(self.checkbox_frame, text=path, variable=var)
            cb.pack(anchor="w")
            self.template_vars[path] = var

        # Select/Deselect All buttons
        self.toggle_frame = ttk.Frame(root)
        self.toggle_frame.pack(pady=(5,10))
        
        ttk.Button(self.toggle_frame, text="Select All", command=self.select_all).pack(side="left", padx=5)
        ttk.Button(self.toggle_frame, text="Deselect All", command=self.deselect_all).pack(side="left", padx=5)
        
        # Control buttons
        self.start_button = ttk.Button(root, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=(0, 5))

        self.stop_button = ttk.Button(root, text="Stop Bot", command=self.stop_bot, state="disabled")
        self.stop_button.pack()

    def start_bot(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.run_bot_loop()

    def stop_bot(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        
    def select_all(self):
        for var in self.template_vars.values():
            var.set(True)
    def deselect_all(self):
        for var in self.template_vars.values():
            var.set(False)

    def capture_screen(self, filename="screen.png"):
        subprocess.run(f"{ADB_PATH} exec-out screencap -p > {filename}", shell=True)
        return cv2.imread(filename)

    def find_button_location(self, screen, template_path):
        template = cv2.imread(template_path)
        if template is None:
            print(f"[!] Could not read template: {template_path}")
            return None

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"→ {template_path} match confidence: {max_val:.3f}")
        if max_val >= CONFIDENCE_THRESHOLD:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return center_x, center_y
        return None

    def tap(self, x, y):
        print(f"👉 Tapping at ({x}, {y})")
        subprocess.run(f"{ADB_PATH} shell input tap {x} {y}", shell=True)
        time.sleep(TAP_DELAY)

    def run_bot_loop(self):
        def loop():
            if not self.running:
                return

            screen = self.capture_screen()
            tapped = False

            for path, var in self.template_vars.items():
                if var.get():  # Only check enabled templates
                    coords = self.find_button_location(screen, path)
                    if coords:
                        self.tap(*coords)
                        tapped = True
                        break

            if not tapped:
                print("…No button found, waiting.")

            self.root.after(2000, loop)

        loop()


if __name__ == "__main__":
    root = ttk.Window(themename="solar") # "darkly", "cyborg", "superhero", "solar", etc.
    app = BotGUI(root)
    root.mainloop()
