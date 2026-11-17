import tkinter as tk
from tkinter import ttk

root = tk.Tk()

""" 
Make a simple gui with tkinter
Make a button that adds to the CSV dataset of what goblin was found and what time it was found.


"""

####################################################
def track_goblin(goblin_type:str):
    """ Records the date, time, and goblin type to the datasheet and console. """
    print("Clicked!")

####################################################
root.title("Goblin Tracker")
root.configure(background="yellow")
root.minsize(200, 200)
root.maxsize(500, 500)
root.geometry("300x300+50+50")

# goblin_type images
img_Treasure_Goblin         = tk.PhotoImage(file=r"./img/Treasure Goblin.png")
img_Blood_Thief             = tk.PhotoImage(file=r"./img/Blood Thief.png")
img_Odious_Collector        = tk.PhotoImage(file=r"./img/Odious Collector.png")
img_Gem_Hoarder             = tk.PhotoImage(file=r"./img/Gem Hoarder.png")
img_Malevolent_Tormentor    = tk.PhotoImage(file=r"./img/Malevolent Tormentor.png")
img_Rainbow_Goblin          = tk.PhotoImage(file=r"./img/Rainbow Goblin.png")
img_Menagerist_Goblin       = tk.PhotoImage(file=r"./img/Menagerist Goblin.png")
img_Gilded_Baron            = tk.PhotoImage(file=r"./img/Gilded Baron.png")
img_Insufferable_Miscreant  = tk.PhotoImage(file=r"./img/Insufferable Miscreant.png")
img_Gelatinous_Sire         = tk.PhotoImage(file=r"./img/Gelatinous Sire.png")

# Buttons
btn_Treasure_Goblin = tk.Button(root, image=img_Treasure_Goblin, command=lambda: track_goblin("Treasure_Goblin"))
btn_Treasure_Goblin.pack(pady=20)
# btn_Blood_Thief
# btn_Odious_Collector
# btn_Gem_Hoarder
# btn_Malevolent_Tormentor
# btn_Rainbow_Goblin
# btn_Menagerist_Goblin
# btn_Gilded_Baron
# btn_Insufferable_Miscreant
# btn_Gelatinous_Sire













root.mainloop()


