# gui.py
# tkinter window and buttons
import tkinter as tk

import tracker
import visualization

COLUMNS = 3


def run_gui() -> None:
    """Builds the goblin tracker window and starts the tkinter loop."""
    root = tk.Tk()
    root.title("Goblin Tracker")
    root.configure(background="gray")
    
    
    ############# Buttons #############
    images = {}
    buttons = {}
    
    # Creates the buttons
    for index, name in enumerate(tracker.GOBLINS):
        # Load images
        img_path = tracker.IMG_DIR / f"{name}.png"
        images[name] = tk.PhotoImage(file=str(img_path))
        
        # Creating buttons
        btn = tk.Button(
            root,
            image=images[name],
            command=lambda g=name: tracker.track_goblin(g)
        )
        
        # Rows and Columns
        row, col = divmod(index, COLUMNS)
        
        # Centering the last goblin
        if index == len(tracker.GOBLINS) - 1 and len(tracker.GOBLINS) % COLUMNS == 1:
            col = 1
        
        btn.grid(row=row, column=col, padx=5, pady=5)
        buttons[name] = btn
        
        
    ######
    # The undo button
    btn_undo = tk.Button(root, text="UNDO LAST ENTRY", command=lambda: tracker.undo_last())
    btn_undo.grid(row=row+1, column=0, padx=5, pady=5)
    
    # The Visualize Button
    btn_visualize = tk.Button(root, text="Graph It", command=visualization.plot_goblins_per_day())
    btn_visualize.grid(row=row+1, column=1, padx=5, pady=5)
    #####
    root.mainloop()
    