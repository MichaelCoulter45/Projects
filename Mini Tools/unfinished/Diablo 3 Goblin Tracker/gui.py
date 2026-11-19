# gui.py
# tkinter window and buttons
import tkinter as tk
from data import GOBLINS, IMG_DIR, track_goblin, undo_last

class GoblinApp:
    def __init__(self, root: tk.Tk, columns: int = 3):
        self.root = root
        root.title("Goblin Tracker")
        root.configure(background="gray")

        self.images = {}   # keep references or tkinter garbage-collects them
        for index, name in enumerate(GOBLINS):
            self.images[name] = tk.PhotoImage(file=str(IMG_DIR / f"{name}.png"))
            row, col = divmod(index, columns)
            if index == len(GOBLINS) - 1 and len(GOBLINS) % columns == 1:
                col = 1
            tk.Button(
                root, image=self.images[name],
                command=lambda g=name: self.on_found(g),
            ).grid(row=row, column=col, padx=5, pady=5)

        self.status = tk.Label(root, text="", bg="gray")
        self.status.grid(row=row + 1, column=0, columnspan=columns)
        tk.Button(root, text="UNDO LAST ENTRY", command=self.on_undo).grid(
            row=row + 2, column=0, padx=5, pady=5)
        tk.Button(root, text="SHOW CHARTS", command=self.on_charts).grid(
            row=row + 2, column=1, padx=5, pady=5)

    def on_found(self, goblin):
        track_goblin(goblin)
        self.status.config(text=f"Logged: {goblin}")

    def on_undo(self):
        removed = undo_last()
        self.status.config(text=f"Removed: {removed[1]}" if removed else "Nothing to undo")

    def on_charts(self):
        from visualization import show_charts   # imported here, so matplotlib loads only when needed
        show_charts()