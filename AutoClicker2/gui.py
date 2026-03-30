import tkinter as tk
from tkinter import ttk
import main


keybind_toggle = '.'








root = tk.Tk()
root.title("Michael's Auto Clicker")

tk.Label(root, text="Game Window:").grid(row=0, column=0, padx=5, pady=5)
window_entry = tk.Entry(root)
window_entry.insert(0,"Window Name")
window_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Clicks Per Second:").grid(row=1, column=0, padx=5, pady=5)
cps_entry = tk.Entry(root)
cps_entry.insert(0,"60")
cps_entry.grid(row=1, column=1, padx=5, pady=10)

tk.Label(root, text=f"Toggle Hotkey: [ {keybind_toggle} ]").grid(row=2, column=0, padx=5, pady=5)

status_label = tk.Label(root, text="ENTER WINDOW NAME", fg="orange")
status_label.grid(row=3, column=0, columnspan=2, pady=5)


start_button = ttk.Button(root, text="✅ Start", command=main.start_bot)
start_button.grid(row=4, column=0, padx=5, pady=5)

quit_button = ttk.Button(root, text="🚫 Quit", command=root.destroy)
quit_button.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()