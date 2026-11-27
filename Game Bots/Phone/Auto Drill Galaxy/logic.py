# logic.py
# 
import subprocess
import time
import cv2
import numpy as np
import pyautogui
import threading


bot_active = False





############################
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
def find(screen, template_path, threshold=0.85):
    """ Find template match """
    tmpl = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        h, w = tmpl.shape
        return (max_loc[0] + w // 2, max_loc[1] + h // 2)  # center point
    return None
#############################
def check_planet():
    """ Checks current planet """
    
#############################
def show_mouse_pos(bot_active:threading.Event, mouse_pos:threading.Event) -> None:
    """ Displays your mouse's postion in the terminal. """
    if  bot_active.is_set():
        mouse_pos.clear()
    else:
        mouse_pos.set()
        print(f"{pyautogui.displayMousePosition()}")

def tap(x,y,amount=1) -> None:
    """ Simulates a tap in bluestacks at (x,y) position and repeats {amount} times."""
    for _ in range(amount):
        subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])


def click_if_found(screen, template, threshold=0.85):
    """ Finds the matching template and clicks it. """
    pos = find(screen, template, threshold)
    if pos:
        tap(*pos)
        return True
    return False
#############################
def observatory():
    """ Collects the observatory points """
def mining():
    """ Attempts the mining minigame """