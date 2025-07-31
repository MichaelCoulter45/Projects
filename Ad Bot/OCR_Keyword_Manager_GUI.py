import os
import cv2
import pytesseract
import numpy as np
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

# === Config ===
ADB_PATH = "C:/Users/power/AppData/Local/Android/Sdk/platform-tools/adb.exe"
CONFIDENCE_THRESHOLD = 0.9
TAP_DELAY = 1.5

# === Global State ===
template_paths = []
ocr_keywords = []
root = tk.Tk()
run_ocr = tk.BooleanVar(value=True)
run_png = tk.BooleanVar(value=True)
run_forever = tk.BooleanVar(value=True)
ocr_runs = tk.IntVar(value=1)
png_runs = tk.IntVar(value=1)

# === Core Functions ===
def capture_screen(filename="screen.png"):
    os.system(f"{ADB_PATH} exec-out screencap -p > {filename}")
    return cv2.imread(filename)

def find_button_location(screen, template_path):
    template = cv2.imread(template_path)
    if template is None:
        print(f"[!] Could not read template: {template_path}")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"→ {template_path} match confidence: {max_val:.3f}")
    if max_val >= CONFIDENCE_THRESHOLD:
        h, w = template.shape[:2]
        # Add slight randomization to tapping area
        offset_x = random.randint(-w // 6, w // 6)
        offset_y = random.randint(-h // 6, h // 6)
        center_x = max_loc[0] + w // 2 + offset_x
        center_y = max_loc[1] + h // 2 + offset_y
        return center_x, center_y
    return None

def tap(x, y):
    print(f"👉 Tapping at ({x}, {y})")
    os.system(f"{ADB_PATH} shell input tap {x} {y}")
    time.sleep(TAP_DELAY)

def run_bot():
    print("🚀 Starting bot...")
    png_counter = 0
    ocr_counter = 0

    while run_forever.get() or (png_counter < png_runs.get() or ocr_counter < ocr_runs.get()):
        screen = capture_screen()

        if run_png.get() and (run_forever.get() or png_counter < png_runs.get()):
            for path in template_paths:
                coords = find_button_location(screen, path)
                if coords:
                    tap(*coords)
                    png_counter += 1
                    break

        if run_ocr.get() and (run_forever.get() or ocr_counter < ocr_runs.get()):
            gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray).lower()
            print(f"[OCR] Found text:\n{text}")
            for keyword in ocr_keywords:
                if keyword.lower() in text:
                    print(f"[OCR] Match found for: {keyword}")
                    # Simulate center tap (approximation)
                    tap(screen.shape[1] // 2 + random.randint(-50, 50),
                        screen.shape[0] // 2 + random.randint(-50, 50))
                    ocr_counter += 1
                    break

        time.sleep(2)

    print("✅ Bot finished running.")

# === GUI Functions ===
def add_png():
    files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg")])
    for file in files:
        if file not in template_paths:
            template_paths.append(file)
            png_list.insert(tk.END, os.path.basename(file))

def remove_selected_png():
    selected = png_list.curselection()
    for index in reversed(selected):
        template_paths.pop(index)
        png_list.delete(index)

def add_keyword():
    word = keyword_entry.get().strip()
    if word and word not in ocr_keywords:
        ocr_keywords.append(word)
        keyword_list.insert(tk.END, word)
        keyword_entry.delete(0, tk.END)

def remove_selected_keyword():
    selected = keyword_list.curselection()
    for index in reversed(selected):
        ocr_keywords.pop(index)
        keyword_list.delete(index)

def start_threaded_bot():
    t = Thread(target=run_bot)
    t.daemon = True
    t.start()

# === GUI ===
#root = tk.Tk()
root.title("📱 Android Auto Tap Bot")
root.geometry("600x500")

# PNG Frame
png_frame = ttk.LabelFrame(root, text="🖼️ PNG Image Templates")
png_frame.pack(fill="x", padx=10, pady=5)

png_list = tk.Listbox(png_frame, height=5)
png_list.pack(side="left", fill="x", expand=True, padx=5)
btn_frame = tk.Frame(png_frame)
btn_frame.pack(side="right", fill="y")
ttk.Button(btn_frame, text="Add", command=add_png).pack(fill="x", pady=2)
ttk.Button(btn_frame, text="Remove", command=remove_selected_png).pack(fill="x", pady=2)

# Keyword Frame
keyword_frame = ttk.LabelFrame(root, text="🔤 OCR Keywords")
keyword_frame.pack(fill="x", padx=10, pady=5)

keyword_list = tk.Listbox(keyword_frame, height=5)
keyword_list.pack(side="left", fill="x", expand=True, padx=5)
key_btn_frame = tk.Frame(keyword_frame)
key_btn_frame.pack(side="right", fill="y")
keyword_entry = ttk.Entry(key_btn_frame)
keyword_entry.pack(fill="x", pady=2)
ttk.Button(key_btn_frame, text="Add", command=add_keyword).pack(fill="x", pady=2)
ttk.Button(key_btn_frame, text="Remove", command=remove_selected_keyword).pack(fill="x", pady=2)

# Settings Frame
settings_frame = ttk.LabelFrame(root, text="⚙️ Settings")
settings_frame.pack(fill="x", padx=10, pady=5)

ttk.Checkbutton(settings_frame, text="Enable PNG Scanning", variable=run_png).pack(anchor="w")
ttk.Checkbutton(settings_frame, text="Enable OCR Scanning", variable=run_ocr).pack(anchor="w")
ttk.Checkbutton(settings_frame, text="Run Forever", variable=run_forever).pack(anchor="w")

ocr_spin = ttk.Spinbox(settings_frame, from_=1, to=1000, textvariable=ocr_runs, width=5)
png_spin = ttk.Spinbox(settings_frame, from_=1, to=1000, textvariable=png_runs, width=5)
ttk.Label(settings_frame, text="OCR Run Count").pack(anchor="w")
ocr_spin.pack(anchor="w")
ttk.Label(settings_frame, text="PNG Run Count").pack(anchor="w")
png_spin.pack(anchor="w")

# Start Button
ttk.Button(root, text="🚀 Start Bot", command=start_threaded_bot).pack(pady=15)

root.mainloop()
