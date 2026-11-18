import tkinter as tk
from tkinter import ttk
from pathlib import Path
import csv
from datetime import datetime

""" 
Make a simple gui with tkinter
Make a button that adds to the CSV dataset of what goblin was found and what time it was found.


"""
root = tk.Tk()
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
DS_DIR = BASE_DIR / "dataset"
DS = DS_DIR / "Diablo 3 goblin tracker.csv"
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
    time = [timestamp, "Event_A", 42]
    
    if goblin_type not in goblins:
        raise ValueError(f"Unknown goblin type: {goblin_type}")
    print(f"Found {goblin_type}!")
    # Writes to CSV
    with DS.open(mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(f"{time}, {goblin_type}")
        
        if not DS_EXISTS:
            writer.writerow(["Timestamp", "Goblin"])
####################################################
root.title("Goblin Tracker")
root.configure(background="gray")



############# Buttons #############
images = {}
buttons = {}
columns = 3
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






#####
root.mainloop()