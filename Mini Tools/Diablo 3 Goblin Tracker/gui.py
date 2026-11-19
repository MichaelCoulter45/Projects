# gui.py
# tkinter window and buttons
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import csv
from datetime import datetime

""" 
* Make a simple gui with tkinter
* Make a button that adds to the CSV dataset of what goblin was found and what time it was found.
* Make an undo button to delete the last (newest) entry.

"""
root = tk.Tk()
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
DS_DIR = BASE_DIR / "dataset"
DS = DS_DIR / "goblin tracker.csv"
DS_EXISTS = DS.exists()

# Goblin Types
goblins = [
    "Treasure Goblin",
    "Blood Thief",
    "Odious Collector",
    "Gem Hoarder",
    "Malevolent Tormentor",
    "Gelatinous Sire",
    "Menagerist Goblin",
    "Gilded Baron",
    "Insufferable Miscreant",
    "Rainbow Goblin",
]
####################################################
def track_goblin(goblin_type:str) -> None:
    """ Records the date, time, and goblin type to the datasheet and console. """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Raise error if invalid goblin type.
    if goblin_type not in goblins:
        raise ValueError(f"Unknown goblin type: {goblin_type}")
    # Writes to CSV
    else:
        print(f"Found {goblin_type}!")
        row_data = [f"{timestamp}", f"{goblin_type}"]
        with DS.open(mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)
######
def undo_last():
    """ Reads the goblin tracker CSV and rewrites the whole thing without the last row for best removal."""
    if not DS_EXISTS:
        raise ValueError(f"Error: File does not exist.")
    else:
        with DS.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if rows:
            print(f"UNDO LAST ENTRY: #{len(rows)}{rows[len(rows)-1]}")
            with DS.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows[:-1])
####################################################
root.title("Goblin Tracker")
root.configure(background="gray")



############# Buttons #############
images = {}
buttons = {}
columns = 3
# Creates the buttons
for index, name in enumerate(goblins):
    # Load images
    img_path = IMG_DIR / f"{name}.png"
    images[name] = tk.PhotoImage(file=str(img_path))
    
    # Creating buttons
    btn = tk.Button(
        root,
        image=images[name],
        command=lambda g=name: track_goblin(g)
    )
    
    # Rows and Columns
    row, col = divmod(index, columns)
    
    # Centering the last goblin
    if index == len(goblins) - 1 and len(goblins) % columns == 1:
        col = 1
    
    btn.grid(row=row, column=col, padx=5, pady=5)
    buttons[name] = btn
    
    
######
# The undo button
btn_undo = tk.Button(root, text="UNDO LAST ENTRY", command= lambda: undo_last())
btn_undo.grid(row=row+1, column=0, padx=5, pady=5)



#####
root.mainloop()
