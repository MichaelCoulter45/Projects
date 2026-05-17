import ctypes
import time
import random

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]

def click():
    extra = ctypes.c_ulong(0)

    down = INPUT(type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra)))

    up = INPUT(type=INPUT_MOUSE,
        mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra)))

    ctypes.windll.user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
    time.sleep(random.uniform(0.045, 0.065))
    ctypes.windll.user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))

# Test loop
time.sleep(5) # Seconds before starting
print("Starting!")
while True:
    click()
    time.sleep(1/60)  # adjust speed