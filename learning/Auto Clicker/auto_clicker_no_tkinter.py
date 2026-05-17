import win32gui, win32api, win32con
import keyboard
import time


# Keybinds
keybind_toggle = '.'
keybind_quit = '/'


# Bot Stuff
bot_running = True
active = False
cps = 200
delay_cpu = 0.1
delay_cps = 1/cps
hwnd = win32gui.FindWindow(None, "GRIM CLICKER")




######            Functions         ######
def toggle_bot():
    global active
    active = not active
    if active:
        print(f"✅ Bot Activated!")
    else:
        print(f"⏸️ Pausing...")


def auto_clicker():
    global bot_running, active, hwnd
    lparam = win32api.MAKELONG(0,0)
    
    
    while bot_running:
        if active:
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(delay_cps)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)            











###########
def main():
    keyboard.add_hotkey(keybind_toggle, toggle_bot)
    auto_clicker()
if __name__ == "__main__":
    main()

