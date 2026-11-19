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