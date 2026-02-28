# Gamblers Table Bot
# Clicks all over the game table randomly and fast to flip coins.

import win32api, win32gui, win32con 
import time
import keyboard
import random
import os, sys
import tkinter as tk

game_window_title = 'Gamblers Table'

# Keybinds
keybind_toggle = '.'
keybind_quit = ','

# Bot stuf
bot_running = True
bot_active = False


# Finding the window
hwnd = win32gui.FindWindow(None, game_window_title)
if not hwnd:
    raise RuntimeError(f"Window {game_window_title} not found!")
left, top, right, bottom = win32gui.GetClientRect(hwnd)

# Clickable Table Area -- Note: (0,0) is the very top left of the screen.
table_left  = right * 0.05      # 5% inward
table_top   = bottom * 0.05     # 5% inward
table_right = right * 0.70      # 70% inward
table_bottom = bottom * 0.80    # 20% inward


################   Bot Operations   ################
def toggle_bot():
    global bot_running, bot_active
    bot_active = not bot_active
    if bot_active:
        print(f"Bot Started!")
    if not bot_active:
        print(f"Bot Paused...")


def stop_bot():
    print(f"Stopping Bot. Goodbye.")
    sys.exit()
####################################################
#############   Bot Functions    ###################

def click(x,y):
    lparam = win32api.MAKELONG(x,y)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x,y, lparam)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x,y, lparam)


def swipe(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.001)


def bot():
    global bot_active
    
    print(f"Bot is ready to start!")
    while bot_running:
        
        if bot_active:
            x = random.randint(int(table_left), int(table_right))
            y = random.randint(int(table_top), int(table_bottom))
            click(x,y)


#######################   GUI   ####################

# def create_gui():
#     """Simple tkinter control window for the bot."""
#     root = tk.Tk()
#     root.title("Gamblers Table Bot")
#     root.geometry("200x120")

#     btn_toggle = tk.Button(root, text="Start / Pause", command=toggle_bot)
#     btn_toggle.pack(padx=10, pady=5)

#     btn_quit = tk.Button(root, text="Quit", command=stop_bot)
#     btn_quit.pack(padx=10, pady=5)

#     def bot_loop():
#         if bot_active:
#             x = random.randint(int(table_left), int(table_right))
#             y = random.randint(int(table_top), int(table_bottom))
#             click(x, y)
#         if bot_running:
#             root.after(1, bot_loop)
#         else:
#             root.quit()

#     root.after(1, bot_loop)
#     root.mainloop()

####################################################

def main():
    keyboard.add_hotkey(keybind_toggle, toggle_bot)
    keyboard.add_hotkey(keybind_quit, stop_bot)
    # create_gui()
    bot()

if __name__ == '__main__':
    main()