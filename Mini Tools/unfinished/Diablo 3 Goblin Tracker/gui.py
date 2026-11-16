import tkinter as tk
from tkinter import ttk

root = tk.Tk()

""" 
Make a simple gui with tkinter
Make a button that adds to the CSV dataset of what goblin was found and what time it was found.

goblin_types
    
"""
img_Treasure_Goblin         = r"./img/Treasure Goblin.png"
img_Blood_Thief             = r"./img/Blood Thief.png"
img_Odious_Collector        = r"./img/Odious Collector.png"
img_Gem_Hoarder             = r"./img/Gem Hoarder.png"
img_Malevolent_Tormentor    = r"./img/Malevolent Tormentor.png"
img_Rainbow_Goblin          = r"./img/Rainbow Goblin.png"
img_Menagerist_Goblin       = r"./img/Menagerist Goblin.png"
img_Gilded_Baron            = r"./img/Gilded Baron.png"
img_Insufferable_Miscreant  = r"./img/Insufferable Miscreant.png"
img_Gelatinous_Sire         = r"./img/Gelatinous Sire.png"
####################################################
def button_goblin(goblin_type:str):
    




####################################################
root.title("Goblin Tracker")
root.configure(background="yellow")
root.minsize(200, 200)
root.maxsize(500, 500)
root.geometry("300x300+50+50")


root.mainloop()


