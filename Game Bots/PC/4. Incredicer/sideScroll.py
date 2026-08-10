# main.py
import win32api
import win32gui
import keyboard
import pyautogui
import time
import sys
import random

game_window_title = "Incredicer"
running = True
bot_active = False

hotkey_mouse_pos = '/'
hotkey_toggle = '.'
hotkey_quit_program = 'q'

delay_cpu = 0.05
delay_mouse_move = 0.01

# Random
#############################################################
def swipe_game_screen():
    global bot_active
    window_size = get_game_window_size(game_window_title)
    x = start_x = window_size['x']
    y = start_y = window_size['y'] + 50
    end_x = window_size['width'] - (window_size['width']*0.20)
    end_y = window_size['height']
    while running:
        if bot_active:
            win32api.SetCursorPos((x,y))
            if x <= end_x:
                x = x + 50
            else:
                x = start_x
                y = y + 150
            if y >= end_y:
                y = start_y
            time.sleep(delay_mouse_move)
        else:
            time.sleep(delay_cpu)
#############################################################
def get_game_window_size(game_window_title):
    hwnd = win32gui.FindWindow(None, game_window_title)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        return {'x': left, 'y': top, 'width': width, 'height': height}
    else:
        print("❌ No window found...")
        return

def mouse_pos():
    print(pyautogui.position())

def toggle_bot():
    global bot_active
    bot_active = not bot_active
    if bot_active:
        print("✅ Bot is active!!")
    else:
        print("⏸️  PAUSING!")

def quit_program():
    global running
    running = False
    print("Quitting. Goodbye!")
    sys.exit(0)
#############################################################
def main():
    keyboard.add_hotkey(hotkey_toggle, toggle_bot)
    keyboard.add_hotkey(hotkey_mouse_pos, mouse_pos)
    keyboard.add_hotkey(hotkey_quit_program, quit_program)
    print("Program is active!!")
    print(f"""
Press {hotkey_toggle} to toggle the bot!
Press {hotkey_mouse_pos} to print the mouse position.
Press {hotkey_quit_program} to quit the program!!""")
    while running:
        swipe_game_screen()
        time.sleep(delay_cpu)
if __name__ == "__main__":
    main()











# Scrap Code
"""


"""