# my_bot1.py

import pyautogui
import cv2
import dxcam
import os
import sys
import time
import keyboard
import random
import threading
from pymem import Pymem

#### GOALS ####
# Reach at least 30 fps for bot frames..
# Thread everything...
###############

# ------------ CONFIG ------------ #
# Constants / Unchangables 
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR_LIVE = os.path.join(BASE_DIR, "templates", "live")
TEMPLATE_DIR_DEAD = os.path.join(BASE_DIR, "templates", "dead")
WINDOW_NAME = "Slime Squisher"
PROCESS_NAME = "Slime_Squisher.exe"
THRESHOLD = 0.70
SCALE = 0.5
DELAY_TOGGLE_BOT = 0.5 # The delay before the button can be registered again..

# Delays / Cooldowns
delay_cpu = 0
delay_click = 0
delay_target_fps = 1/30

# Bot
bot_active = False
frame_counter_enabled = True

# Hotkeys
hotkey_toggle_bot = 'P'
hotkey_exit_bot = 'Q'
####################################
# ------------ METHODS ----------- #
def click_mouse(x,y):
    original_pos = pyautogui.position()
    pyautogui.moveTo(random.randrange(x-5, x+5), random.randrange(y-5, y+5)) # Slight variability for human-likeness - for fun..
    # pyautogui.click()
    print(f"✅ Clicked!")
    pyautogui.moveTo(original_pos)
    time.sleep(delay_click)


def toggle_bot():
    global bot_active
    bot_active = not bot_active
    if bot_active:
        print(f"The Bot has been activated!")
    else:
        print(f"PAUSING Bot...")



def dxcam_cam():
    
    time.sleep(delay_target_fps)



def matching():
    
    time.sleep(delay_cpu)


# ------------ Main Bot ----------- #
def main_bot():
    global bot_active
    bot_frame_skip = 2
    frame_counter = 0
    #### Header ####
    while True:
        while bot_active == True: # While the bot is active
            frame_counter += 1
            print(frame_counter)
            
            #### Bot Body ####
            #### Frame Skipping ####
            if frame_counter % bot_frame_skip == 0 and frame_counter_enabled: # Enables frame skipping for freeing cpu processing
                k = 1 # placeholder text
                click_mouse(500, 500)
                
                
                
                
                
                
                time.sleep(delay_cpu) # Cooldown per active bot frame loop
            elif not frame_counter_enabled:
                k = 1 # placeholder text
                pass
            else:
                pass
            #### End of Frame Skipping ####
            
            #### Tail ####
        time.sleep(delay_cpu) # Cooldown per "while True" loop
####################################
# -------------- RUN ------------- #
if __name__ == "__main__":
    #### Header ####
    main_bot_thread = threading.Thread(target=main_bot, daemon=True)
    matching_thread = threading.Thread(target=matching, daemon=True)
    
    main_bot_thread.start()
    matching_thread.start()
    print(f"Press {hotkey_toggle_bot} to Toggle the bot and {hotkey_exit_bot} to Exit the program!")
    #### Body ####
    while True:
        # Keybinds
        if keyboard.is_pressed(hotkey_toggle_bot):
            toggle_bot()
            time.sleep(DELAY_TOGGLE_BOT)
        if keyboard.is_pressed(hotkey_exit_bot):
            print(f"Program Terminated")
            sys.exit()
            break
    ### End of Main While Loop ###
####################################