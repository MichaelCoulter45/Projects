import win32api, win32con, win32gui
import time
import keyboard
import sys
import pyautogui

#############################################
window_title = "Kiwi Clicker"
running = True
bot_active = False
upgrade_count = 0

keybind_quit = 'Q'
keybind_toggle_bot = '.'
keybind_mouse_pos = '/'

delay_cpu = 0.01
delay_click = 0.01

############## Program Functionals ###############################
def get_window_size():
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        return {'x': left,'y':top,'width':width,'height':height}
    else:
        print("❌ No window found.")
        return

def toggle_bot():
    global bot_active
    bot_active = not bot_active
    if bot_active:
        print("✅ Bot is active!")
    else:
        print("⏸️  PAUSING...")

def quit_program():
    global running
    running = False
    print("Quitting. Goodbye!")
    sys.exit(0)
################# Base Functionals ############################
def get_mouse_pos():
    print(pyautogui.position())

def move_mouse(x,y):
    win32api.SetCursorPos((x,y))

def click(amount=25, repeat=1):
    global bot_active
    for i in range(amount*repeat):
        if not bot_active:
            break
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0)
            time.sleep(0.00001)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0)
        
        time.sleep(delay_click)
################# Game Functions ############################
def click_kiwi():
    move_mouse(945,620)
    click()
def click_security():
    move_mouse(955,350)
    click()
def click_target():
    move_mouse(1545,740)
    click(10)
def click_upgrades():
    global upgrade_count
    if upgrade_count == 1: # Kiwi Bags
        move_mouse(250,580)
        click(1)
        move_mouse(440,500)
        click(1)
        move_mouse(600,485)
        click(1)
        print(f"Upgraded: Kiwi Bags")
    elif upgrade_count == 2: # Security
        move_mouse(725,535)
        click(1)
        move_mouse(1010,433)
        click(1)
        print(f"Upgraded: Security")
    elif upgrade_count == 3: # Kiwi Clicks
        move_mouse(960,925)
        click(1)
        move_mouse(1145,830)
        click(1)
        print(f"Upgraded: Kiwi Clicks")
    elif upgrade_count == 4: # Clicker Car
        move_mouse(1290,785)
        click(1)
        move_mouse(1285,680)
        click(1)
        print(f"Upgraded: Car")
    elif upgrade_count == 5: # Castle
        move_mouse(1790,520)
        click(1)
        move_mouse(1770,420)
        click(1)
        print(f"Upgraded: Castle")
        upgrade_count = 0
    upgrade_count +=1
################ Main Bot Loop #############################
def bot_loop():
    global running
    global bot_active
    
    while running:
        if bot_active:
            
            for i in range(5):
                click_kiwi()
                click_security()
                click_target()
                
            click_upgrades()
            time.sleep(delay_cpu)
#############################################
def main():
    global running
    keyboard.add_hotkey(keybind_quit, quit_program)
    keyboard.add_hotkey(keybind_toggle_bot, toggle_bot)
    keyboard.add_hotkey(keybind_mouse_pos, get_mouse_pos)
    print(f""" 
    ‼️ Program Running!
        Press {keybind_mouse_pos} to get the mouse pos.
        Press {keybind_toggle_bot} to toggle the bot.
        Press {keybind_quit} to quit the program!
        """)
    while running:
        bot_loop()
if __name__ == "__main__":
    main()