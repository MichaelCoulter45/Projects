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
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# OCR and PNG matching settings
ocr_keywords = []
template_paths = []
running = False
auto_tapper_running = False
auto_tap_coords = (100, 100) # default tap location
preview_height = 500
preview_width = 300
# OCR and PNG matching settings

tap_cooldown_value = 0.1 # Each cycle takes about 3 seconds anyway.
capture_interval_value = 0.1

# --- Tapping Feature ---#
def adb_tap(x, y):
    cmd = f"adb shell input tap {x} {y}"
    os.system(cmd)
    log(f"[Tap] Sent tap at ({x}, {y})")

def start_auto_tapper():
    global auto_tapper_running
    auto_tapper_running = True
    def tap_loop():
        while auto_tapper_running:
            adb_tap(*auto_tap_coords)
            time.sleep(1.0)
    threading.Thread(target=tap_loop, daemon=True).start()

def stop_auto_tapper():
    global auto_tapper_running
    auto_tapper_running = False
# --- Tapping Feature ---#    



# --- Capture and Processing Functions --- #
def get_phone_screen():
    try:
        result = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            print(f"[!] ADB screencap failed")
            return None
        img_bytes = result.stdout
        # Convert to PIL image from bytes
        return Image.open(BytesIO(img_bytes))
    except Exception as e:
        print(f"[!] Failed to capture screen: {e}")
        return None

def resize_to_fit(image, max_width=720, max_height=1440):
    w,h = image.size
    scale = min(max_width / w, max_height / h)
    new_sizr = (int(w * scale), int(h * scale))
    return image.resize(new_sizr, Image.ANTIALIAS)

def capture_screen():
    img = get_phone_screen()
    if img is None:
        return None
    # try:
    #     screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # except Exception as e:
    #     print(f"[!] Failed to convery screenshot to BGR: {e}")
    #     return None
    try:
        # Show preview in the GUI
        # img_tk = ImageTk.PhotoImage(Image.fromarray(screen).resize((preview_width, preview_height)))
        # preview_label.configure(image=img_tk)
        # preview_label.imgtk = img_tk
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"[!] Failed to update preview: {e}")
        return None

def update_preview():
    try:
        screen = get_phone_screen()
        resized = screen.resize((preview_width, preview_height)) 
        preview_img = ImageTk.PhotoImage(resized)
        # preview_label.config(image=preview_img)
        # preview_label.image = preview_img
        img_tk = ImageTk.PhotoImage(preview_img)
        preview_label.configure(image=img_tk)
        preview_label.imgtk = img_tk
        preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))
    except Exception as e:
        print(f"Error updating preview: {e}")

def save_screenshot():
    screen_img = get_phone_screen()
    if screen_img:
        file_path = filedialog.asksaveasfilename(defaultextension="1. Saved Screenshot.png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            try:
                screen_img.save(file_path)
                # messagebox.showinfo("Saved", f"Screenshot saved to: \n{file_path}") # Pops a window up that says Sucessfully saved.
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: \n{e}")

def match_and_tap_templates(screen):
    for path in template_paths:
        if not os.path.exists(path):
            continue
        template = cv2.imread(path, 0)
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)
        match_points = list(zip(*loc[::-1])) # list of (x, y)
        
        # Group nearby matches to suppress duplicates
        filtered = []
        threshold = 30 # Minimum distance between unique taps
        for pt in match_points:
            too_close = False
            for f in filtered:
                if abs(pt[0] - f[0]) < threshold and abs(pt[1] - f[1]) < threshold:
                    too_close = True
                    break
            if not too_close:
                filtered.append(pt)
                
        # Draw and store the final matches
        for pt in filtered:
            cv2.rectangle(screen, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
            center_x = pt[0] + template.shape[1] // 2
            center_y = pt[1] + template.shape[0] // 2
            cv2.circle(screen, (center_x, center_y), 5, (0, 0, 255), -1) # Red Dot for tap point
            log(f"Matched template: {os.path.basename(path)} at ({pt[0]}, {pt[1]})")
            if enable_taps.get():
                adb_tap(center_x, center_y)
            # time.sleep(0.1) # Slight delay between taps
            return screen, (center_x, center_y) # return after first match
    return screen, None

def extract_text(screen):
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text
# --- Capture and Processing Functions --- #



# --- Bot Logic --- #
def run_bot():
    global running
    running = True
    status_label.config(text="🟢 Running", foreground="green")
    def task():
        while running:
            start = time.perf_counter()
            screen = capture_screen()
            if screen is None:
                print("[!] Screen capture failed. Retrying...")
                time.sleep(capture_interval.get())
                continue
            if run_png.get():
                screen, match_point = match_and_tap_templates(screen)
            else:
                match_point = None
            if run_ocr.get():
                text = extract_text(screen)
                for word in ocr_keywords:
                    if word.lower() in text.lower():
                        log(f"Keyword matched: {word}")
                        if match_point is not None and enable_taps.get():
                            x, y = match_point
                            adb_tap(x, y) # Change this to fit needs
                            log(f"[Cooldown] Tap sent, waiting for app to update...")
                            time.sleep(0.5)  # enough time for app to load new UI
            # Update GUI Preview
            preview_img = Image.fromarray(cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            preview_img = preview_img.resize((preview_width, preview_height))
            img_tk = ImageTk.PhotoImage(preview_img)
            # preview_label.imgtk = img_tk
            # preview_label.configure(image=img_tk)
            img_tk = ImageTk.PhotoImage(preview_img)
            preview_label.configure(image=img_tk)
            preview_label.imgtk = img_tk
            preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))
            
            if not background_mode.get():
                break
            # Wait between cycles
            time.sleep(capture_interval.get())
            
            # --- Debugging --- #
            # Measuring time for each loop.
            end = time.perf_counter()
            print(f"Cycle duration: {end - start:.2f} sec")
    threading.Thread(target=task, daemon=True).start()

def stop_bot():
    global running
    running = False
    status_label.config(text="🛑 Stopped", foreground="red")
# --- Bot Logic --- #

# --- Save/Load Profile --- #
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

        #messagebox.showinfo("Loaded", "Profile loaded successfully!")
# --- Save/Load Profile --- #

# --- GUI Setup --- #
root = tk.Tk()
root.title("OCR + PNG Bot")
# Main layout split into left (controls) and right (preview)
main_frame = tk.Frame(root)
main_frame.pack(fill = "both", expand=True)

left_panel = tk.Frame(main_frame)
left_panel.pack(side="left", fill="y")

right_panel = tk.Frame(main_frame)
right_panel.pack(side="right", fill="both", expand=True)

interval_frame = ttk.Frame(left_panel)
interval_frame.pack()

run_ocr = tk.BooleanVar(value=True)
run_png = tk.BooleanVar(value=True)
background_mode = tk.BooleanVar(value=True)
capture_interval = tk.DoubleVar(value=capture_interval_value)

ttk.Label(left_panel, text="OCR Keywords").pack()
keyword_list = tk.Listbox(left_panel)
keyword_list.pack()
# --- GUI Setup --- #

# --- GUI Items --- #
# Log Window 
ttk.Label(right_panel, text="Status Log").pack()
log_text = tk.Text(right_panel, height=10, width=35)
log_text.pack()
def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    
ttk.Label(left_panel, text="Auto Tapper (x, y)").pack()
auto_x = tk.IntVar(value=100)
auto_y = tk.IntVar(value=100)
ttk.Entry(left_panel, textvariable=auto_x, width=5).pack(side="left", padx=2)
ttk.Entry(left_panel, textvariable=auto_y, width=5).pack(side="left", padx=5)
ttk.Button(left_panel, text="▶️ Start Auto Tapper", command=lambda: (set_auto_coords(), start_auto_tapper())).pack()
ttk.Button(left_panel, text="⏹️ Stop Auto Tapper", command=stop_auto_tapper).pack()

def set_auto_coords():
    global auto_tap_coords
    auto_tap_coords = (auto_x.get(), auto_y.get())

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

keyword_entry = ttk.Entry(left_panel)
keyword_entry.pack()
ttk.Button(left_panel, text="Add Keyword", command=add_keyword).pack()
ttk.Button(left_panel, text="Remove Selected", command=remove_keyword).pack()

ttk.Label(left_panel, text="PNG Templates").pack()
png_list = tk.Listbox(left_panel)
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

ttk.Button(left_panel, text="Add Template(s)", command=add_template).pack()
ttk.Button(left_panel, text="Remove Selected", command=remove_template).pack()

# --- Options --- #
ttk.Checkbutton(left_panel, text="Run OCR", variable=run_ocr).pack()
ttk.Checkbutton(left_panel, text="Run PNG Match", variable=run_png).pack()
ttk.Checkbutton(left_panel, text="Background Mode", variable=background_mode).pack()

enable_taps = tk.BooleanVar(value=True)
ttk.Checkbutton(left_panel, text="Enable Taps", variable=enable_taps).pack()

tap_cooldown = tk.DoubleVar(value=tap_cooldown_value)
ttk.Label(left_panel, text="Tap Cooldown (s)").pack()
ttk.Entry(left_panel, textvariable=tap_cooldown, width=5).pack()

ttk.Label(left_panel, text="Capture Interval (s)").pack()
ttk.Entry(left_panel, textvariable=capture_interval, width=5).pack()
# --- Options --- #

# --- Buttons --- #
ttk.Button(left_panel, text="▶ Start Bot", command=run_bot).pack(pady=5)
ttk.Button(left_panel, text="⏹ Stop Bot", command=stop_bot).pack()
profile_frame = ttk.Frame(left_panel)
profile_frame.pack(pady=5)

ttk.Button(profile_frame, text="💾 Save Profile", command=save_profile).pack(side="left", padx=10)
ttk.Button(profile_frame, text="📂 Load Profile", command=load_profile).pack(side="left", padx=10)
ttk.Button(left_panel, text="💾 Save Screenshot", command=save_screenshot).pack(pady=5)
status_label = ttk.Label(left_panel, text="🛑 Stopped", foreground="red")
status_label.pack(pady=5)
# --- Buttons --- #
# --- GUI Items --- #

########### Scroll Bars ####################
preview_frame = tk.Frame(right_panel)
preview_frame.pack(pady=10, fill="both", expand=True)

preview_canvas = tk.Canvas(preview_frame, width=400, height=600)
preview_canvas.pack(side="left", fill="both", expand=True)

scrollbar_y = tk.Scrollbar(preview_frame, orient="vertical", command=preview_canvas.yview)
scrollbar_y.pack(side="right", fill="y")
scrollbar_x = tk.Scrollbar(preview_frame, orient="horizontal", command=preview_canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")

preview_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# This will be your updated label inside the canvas
preview_label = tk.Label(preview_canvas)
preview_window = preview_canvas.create_window((0, 0), window=preview_label, anchor="nw")

# Scroll region update on image size change
def update_scroll_region(event=None):
    preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))

preview_label.bind("<Configure>", update_scroll_region)
########### Scroll Bars ####################

#time.sleep(tap_cooldown.get()) # Puts a delay on the whole program - set in GUI

root.mainloop()



###### Features to add #########
# Add better de-bugging
# Add Matching found for OCR.

###### Organization ############
# add navigation commands vs interaction commands ie: going to the home screen vs tapping activating an ad.
# Re-organize code
# Re-order things in gui to look nice
