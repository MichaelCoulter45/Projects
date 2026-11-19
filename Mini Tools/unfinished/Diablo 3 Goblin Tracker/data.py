# data.py
# CSV read/write, goblin list, paths
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"
DS_DIR = BASE_DIR / "dataset"
DS = DS_DIR / "goblin tracker.csv"

GOBLINS = [
    "Treasure Goblin", "Blood Thief", "Odious Collector", "Gem Hoarder",
    "Malevolent Tormentor", "Gelatinous Sire", "Menagerist Goblin",
    "Gilded Baron", "Insufferable Miscreant", "Rainbow Goblin",
]

def track_goblin(goblin_type: str) -> None:
    if goblin_type not in GOBLINS:
        raise ValueError(f"Unknown goblin type: {goblin_type}")
    DS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with DS.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([timestamp, goblin_type])

def read_entries() -> list[list[str]]:
    if not DS.exists():
        return []
    with DS.open("r", newline="", encoding="utf-8") as f:
        return list(csv.reader(f))

def undo_last() -> list[str] | None:
    """Removes the newest row and returns it (or None if empty)."""
    rows = read_entries()
    if not rows:
        return None
    with DS.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows[:-1])
    return rows[-1]