# data.py
# Paths, goblin list, CSV functions
from pathlib import Path
import csv
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
DS_DIR = BASE_DIR / "dataset"
DS = DS_DIR / "goblin tracker.csv"


# Goblin Types
GOBLINS = [
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
    if goblin_type not in GOBLINS:
        raise ValueError(f"Unknown goblin type: {goblin_type}")
    
    # Writes to CSV
    print(f"Found {goblin_type}!")
    DS_DIR.mkdir(exist_ok=True)
    with DS.open(mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, goblin_type])
######
def undo_last():
    """ Reads the goblin tracker CSV and rewrites the whole thing without the last row for best removal."""
    if not DS.exists():
        raise ValueError(f"Error: File does not exist.")
    
    with DS.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    
    if rows:
        print(f"UNDO LAST ENTRY: #{len(rows)}: {rows[-1]}")
        with DS.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows[:-1])
####################################################
