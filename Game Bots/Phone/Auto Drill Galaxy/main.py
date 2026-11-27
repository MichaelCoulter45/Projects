# main.py
# 
""" This is based on using assigning ADP to the Bluestacks emulator """
""" 
Some terminal commands:
adb connect 127.0.0.1:5555 
C:\platform-tools\adb.exe devices
"""
import keyboard
import time
import threading

import decider
import gui
import logic


# Hotkeys
hotkey_pause = '.'
hotkey_show_mouse_pos = ']'



#############################
def run() -> None:
    """ The main bot loop """
    bot_active = threading.Event()
    bot_active.set()
    mouse_pos = threading.Event()
    
    keyboard.add_hotkey(hotkey_pause, logic.toggle_bot, args=(bot_active,))
    keyboard.add_hotkey(hotkey_show_mouse_pos, logic.show_mouse_pos, args=(bot_active, mouse_pos))
    while True:
        while bot_active.is_set():
            print(f"\tActive")
            time.sleep(1)
            ###
        
        ###
        time.sleep(0.1)

if __name__ == "__main__":
    run()
