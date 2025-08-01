import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import subprocess
import threading
import time
import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab, Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# OCR and PNG matching settings
ocr_keywords = []
template_paths = []
running = False


def get_phone_screen():
    os.system("adb exec-out screencap -p > screen.png")
    try:
        return Image.open("screen.png")
    except Exception as e:
        print(f"[!] Failed to open screen.png: {e}")
        return None

def update_preview():
    try:
        screen = get_phone_screen()
        resized = screen.resize((480, 960)) # change to resize
        preview_img = ImageTk.PhotoImage(resized)
        preview_label.config(image=preview_img)
        preview_label.image = preview_img
    except Exception as e:
        print(f"Error updating preview: {e}")
        
# --- Capture and Processing Functions ---
def capture_screen():
    img = get_phone_screen()
    try:
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"[!] Failed to convery screenshot to BGR: {e}")
        return None
    try:
        # Show preview in the GUI
        img_tk = ImageTk.PhotoImage(Image.fromarray(screen).resize((300, 200)))
        preview_label.imgtk = img_tk # Prevents garbage collection
        preview_label.configure(image=img_tk)
        return screen
    except Exception as e:
        print(f"[!] Failed to update preview: {e}")
    return screen

def match_templates(screen):
    for path in template_paths:
        if not os.path.exists(path):
            continue
        template = cv2.imread(path, 0)
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)
        if np.any(result >= 0.8):
            for pt in zip(*loc[::-1]):
                cv2.rectangle(screen, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
                print(f"Matched template: {os.path.basename(path)} at {pt}")
    return screen

def extract_text(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# --- Bot Logic ---
def run_bot():
    global running
    running = True
    def task():
        while running:
            screen = capture_screen()
            if screen is None:
                print("[!] Screen capture failed. Retrying...")
                time.sleep(capture_interval.get())
                continue
            if run_png.get():
                screen = match_templates(screen)
            if run_ocr.get():
                text = extract_text(screen)
                for word in ocr_keywords:
                    if word.lower() in text.lower():
                        print(f"Keyword matched: {word}")
                        
            preview_img = Image.fromarray(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            preview_img = preview_img.resize((300,200))
            img_tk = ImageTk.PhotoImage(preview_img)
            preview_label.imgtk = img_tk
            preview_label.configure(image=img_tk)
            
            if not background_mode.get():
                break
            time.sleep(capture_interval.get())
    threading.Thread(target=task, daemon=True).start()

def stop_bot():
    global running
    running = False

# --- Save/Load Profile ---
def save_profile():
    profile = {
        "ocr_keywords": ocr_keywords,
        "template_paths": template_paths
    }
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w") as f:
            json.dump(profile, f, indent=4)
        messagebox.showinfo("Saved", "Profile saved successfully!")

def load_profile():
    global ocr_keywords, template_paths
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", ".json")])
    if file_path:
        with open(file_path, "r") as f:
            profile = json.load(f)
        ocr_keywords = profile.get("ocr_keywords", [])
        template_paths = profile.get("template_paths", [])

        keyword_list.delete(0, tk.END)
        for word in ocr_keywords:
            keyword_list.insert(tk.END, word)

        png_list.delete(0, tk.END)
        for path in template_paths:
            png_list.insert(tk.END, os.path.basename(path))

        messagebox.showinfo("Loaded", "Profile loaded successfully!")

# --- GUI Setup ---
root = tk.Tk()
root.title("OCR + PNG Bot")

run_ocr = tk.BooleanVar(value=True)
run_png = tk.BooleanVar(value=True)
background_mode = tk.BooleanVar(value=True)
capture_interval = tk.DoubleVar(value=1.0)

ttk.Label(root, text="OCR Keywords").pack()
keyword_list = tk.Listbox(root)
keyword_list.pack()

preview_label = tk.Label(root)
preview_label.pack(pady=10)


def add_keyword():
    keyword = keyword_entry.get()
    if keyword:
        ocr_keywords.append(keyword)
        keyword_list.insert(tk.END, keyword)
        keyword_entry.delete(0, tk.END)

def remove_keyword():
    selected = keyword_list.curselection()
    for i in reversed(selected):
        del ocr_keywords[i]
        keyword_list.delete(i)

keyword_entry = ttk.Entry(root)
keyword_entry.pack()
ttk.Button(root, text="Add Keyword", command=add_keyword).pack()
ttk.Button(root, text="Remove Selected", command=remove_keyword).pack()

ttk.Label(root, text="PNG Templates").pack()
png_list = tk.Listbox(root)
png_list.pack()


def add_template():
    paths = filedialog.askopenfilenames(filetypes=[("PNG Files", "*.png")])
    for path in paths:
        template_paths.append(path)
        png_list.insert(tk.END, os.path.basename(path))

def remove_template():
    selected = png_list.curselection()
    for i in reversed(selected):
        del template_paths[i]
        png_list.delete(i)

ttk.Button(root, text="Add Template(s)", command=add_template).pack()
ttk.Button(root, text="Remove Selected", command=remove_template).pack()

# --- Options ---
ttk.Checkbutton(root, text="Run OCR", variable=run_ocr).pack()
ttk.Checkbutton(root, text="Run PNG Match", variable=run_png).pack()
ttk.Checkbutton(root, text="Background Mode", variable=background_mode).pack()

interval_frame = ttk.Frame(root)
interval_frame.pack()
ttk.Label(interval_frame, text="Capture Interval (s)").pack(side="left")
ttk.Entry(interval_frame, textvariable=capture_interval, width=5).pack(side="left")

# --- Buttons ---
ttk.Button(root, text="▶ Start Bot", command=run_bot).pack(pady=5)
ttk.Button(root, text="⏹ Stop Bot", command=stop_bot).pack()

profile_frame = ttk.Frame(root)
profile_frame.pack(pady=5)
ttk.Button(profile_frame, text="💾 Save Profile", command=save_profile).pack(side="left", padx=10)
ttk.Button(profile_frame, text="📂 Load Profile", command=load_profile).pack(side="left", padx=10)

root.mainloop()
