# logic.py
# 
import subprocess
import time
import cv2
import numpy as np


bot_active = False

# Hotkeys
hotkey_pause = '.'
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
    


def tap(x,y,amount=1):
    for i in range(amount):
        subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])


def click_if_found(screen, template, threshold=0.85):
    pos = find(screen, template, threshold)
    if pos:
        tap(*pos)
        return True
    return False

#############################
