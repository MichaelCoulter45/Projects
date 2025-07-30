import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
import pyautogui
import time
import threading
import pytesseract

# Tell pytesseract where the executable is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === GUI SETUP ===
root = tk.Tk()
root.title("Template Bot")
root.geometry("700x500")
root.resizable(False, False)

# Template storage (path → {"name": ..., "enabled": True/False})
template_data = {}

# === TEMPLATE MANAGEMENT FRAME ===
template_frame = ttk.LabelFrame(root, text="Templates", padding=10)
template_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Table (Treeview) with columns
columns = ("enabled", "name", "path")
template_tree = ttk.Treeview(template_frame, columns=columns, show="headings", selectmode="browse")
template_tree.heading("enabled", text="✓")
template_tree.heading("name", text="Name")
template_tree.heading("path", text="File Path")
template_tree.column("enabled", width=30, anchor="center")
template_tree.column("name", width=150)
template_tree.column("path", width=400)
template_tree.grid(row=0, column=0, columnspan=4, sticky="nsew")

# === TEMPLATE BUTTON FUNCTIONS ===
def add_template():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if filepath:
        name = os.path.basename(filepath)
        template_data[filepath] = {"name": name, "enabled": True}
        template_tree.insert("", "end", values=("✔", name, filepath))

def remove_template():
    selected = template_tree.selection()
    if selected:
        item = selected[0]
        filepath = template_tree.item(item)["values"][2]
        template_tree.delete(item)
        template_data.pop(filepath, None)

def rename_template():
    selected = template_tree.selection()
    if selected:
        item = selected[0]
        old_name = template_tree.item(item)["values"][1]
        new_name = simpledialog.askstring("Rename Template", "Enter new name:", initialvalue=old_name)
        if new_name:
            filepath = template_tree.item(item)["values"][2]
            template_data[filepath]["name"] = new_name
            template_tree.item(item, values=("✔" if template_data[filepath]["enabled"] else "✘", new_name, filepath))

def toggle_enabled():
    selected = template_tree.selection()
    if selected:
        item = selected[0]
        filepath = template_tree.item(item)["values"][2]
        current_state = template_data[filepath]["enabled"]
        template_data[filepath]["enabled"] = not current_state
        symbol = "✔" if not current_state else "✘"
        template_tree.set(item, column="enabled", value=symbol)

# === TEMPLATE BUTTONS ===
ttk.Button(template_frame, text="➕ Add", command=add_template).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(template_frame, text="❌ Remove", command=remove_template).grid(row=1, column=1, padx=5, pady=5)
ttk.Button(template_frame, text="🖊 Rename", command=rename_template).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(template_frame, text="✔/✘ Toggle", command=toggle_enabled).grid(row=1, column=3, padx=5, pady=5)

# === BOT LOGIC ===
def run_bot():
    # Get enabled template paths
    enabled_templates = [path for path, data in template_data.items() if data["enabled"]]

    if not enabled_templates:
        messagebox.showwarning("No Templates", "Please enable at least one template before starting.")
        return

    # Disable the start button
    start_button.config(state="disabled")

    def bot_loop():
        while True:
            for path in enabled_templates:
                location = pyautogui.locateCenterOnScreen(path, confidence=0.8)
                if location:
                    pyautogui.click(location)
                    print(f"Clicked: {template_data[path]['name']}")
                    time.sleep(1)
            time.sleep(1)

    threading.Thread(target=bot_loop, daemon=True).start()

# === START BUTTON ===
start_button = ttk.Button(root, text="▶️ Start Bot", command=run_bot)
start_button.grid(row=1, column=0, pady=10)

# Run the GUI event loop
root.mainloop()
