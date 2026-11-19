# main.py
# main entry point for the program
import tkinter as tk
from gui import GoblinApp

def main():
    root = tk.Tk()
    GoblinApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()