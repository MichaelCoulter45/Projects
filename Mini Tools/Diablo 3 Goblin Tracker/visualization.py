# visualization.py
# charts built from the csv
from collections import Counter
import matplotlib.pyplot as plt
from data import read_entries

def show_charts():
    rows = read_entries()
    if not rows:
        return
    counts = Counter(goblin for _, goblin in rows)
    plt.barh(list(counts.keys()), list(counts.values()))
    plt.title("Goblins found")
    plt.tight_layout()
    plt.show()