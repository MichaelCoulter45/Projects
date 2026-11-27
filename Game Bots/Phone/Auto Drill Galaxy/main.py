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




hotkey_pause = '.'


def toggle_bot(active_event:threading.Event) -> None:
    """ Toggles the bot active/inactive """
    if active_event.is_set():
        active_event.clear()
        print(f"Bot PAUSED")
    else:
        active_event.set()
        print(f"Bot ACTIVE")

def quit_bot():
    """ Ends the program """
    




#############################
def run() -> None:
    """ The main bot loop """
    bot_active = threading.Event()
    bot_active.set()
    
    keyboard.add_hotkey(hotkey_pause, toggle_bot, args=(bot_active,))
    while True:
        while bot_active.is_set():
            print("1 Second")
            time.sleep(1)
            ###
        
        ###
        time.sleep(0.1)

if __name__ == "__main__":
    run()
