import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pytesseract
from PIL import ImageGrab, Image
import threading
import time
import json

# Internal state for OCR keywords
ocr_keywords = {}

# Load saved profile (if exists)
def load_profile(profile_name="default"):
    global ocr_keywords
    try:
        with open(f"profiles/{profile_name}.json", "r") as f:
            data = json.load(f)
            ocr_keywords = data.get("ocr_keywords", {})
    except FileNotFoundError:
        ocr_keywords = {}

def save_profile(profile_name="default"):
    data = {
        "ocr_keywords": ocr_keywords
    }
    with open(f"profiles/{profile_name}.json", "w") as f:
        json.dump(data, f, indent=4)

def add_keyword():
    word = keyword_entry.get().strip()
    mode = mode_var.get()
    limit = None
    if mode == "n":
        try:
            limit = int(limit_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Limit must be an integer")
            return
    if word:
        ocr_keywords[word] = {"active": True, "mode": mode, "count": 0, "limit": limit}
        update_keyword_list()
        keyword_entry.delete(0, tk.END)
        limit_entry.delete(0, tk.END)

# GUI update

def update_keyword_list():
    for widget in keyword_frame.winfo_children():
        widget.destroy()
    for word, settings in ocr_keywords.items():
        var = tk.BooleanVar(value=settings["active"])

        def make_toggle(word):
            return lambda: toggle_keyword(word, var.get())

        cb = tk.Checkbutton(keyword_frame, text=word, variable=var, command=make_toggle(word))
        cb.pack(anchor="w")

        meta = f"Mode: {settings['mode']} | Count: {settings['count']}"
        if settings["mode"] == "n":
            meta += f" / {settings['limit']}"
        label = tk.Label(keyword_frame, text=meta, font=("Arial", 8), fg="gray")
        label.pack(anchor="w", padx=20)

def toggle_keyword(word, is_active):
    if word in ocr_keywords:
        ocr_keywords[word]["active"] = is_active

# GUI setup

root = tk.Tk()
root.title("OCR Keyword Manager")
root.geometry("400x500")

# Keyword entry
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

tk.Label(entry_frame, text="Keyword:").grid(row=0, column=0)
keyword_entry = tk.Entry(entry_frame)
keyword_entry.grid(row=0, column=1)

mode_var = tk.StringVar(value="once")
tk.Label(entry_frame, text="Mode:").grid(row=1, column=0)
mode_menu = ttk.Combobox(entry_frame, textvariable=mode_var, values=["once", "n", "infinite"], width=10)
mode_menu.grid(row=1, column=1)

limit_entry = tk.Entry(entry_frame)
limit_entry.grid(row=2, column=1)
tk.Label(entry_frame, text="n-times (only if mode=n):").grid(row=2, column=0)

tk.Button(entry_frame, text="Add Keyword", command=add_keyword).grid(row=3, column=0, columnspan=2, pady=5)

# Keyword list
keyword_frame = tk.Frame(root)
keyword_frame.pack(pady=10, fill="both", expand=True)

# Save/Load buttons
profile_frame = tk.Frame(root)
profile_frame.pack(pady=10)

tk.Button(profile_frame, text="Save Profile", command=save_profile).pack(side="left", padx=5)
tk.Button(profile_frame, text="Load Profile", command=load_profile).pack(side="left", padx=5)

# Start
load_profile()
update_keyword_list()
root.mainloop()
