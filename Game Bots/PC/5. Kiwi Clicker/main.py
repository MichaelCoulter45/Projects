import win32api, win32con, win32gui
import time
import keyboard
import sys
import pyautogui
import random

#############################################
window_title = "Kiwi Clicker"
running = True
bot_active = False

keybind_quit = 'Q'
keybind_toggle_bot = '.'
keybind_mouse_pos = '/'

delay_cpu = 0.01
delay_click = 0.01

profession = 0
upgrade_count = 0

############## Program Functions ###############################
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
################# Base Functions ############################
def get_mouse_pos():
    x,y = pyautogui.position()
    print(f"{x},{y}")
    time.sleep(delay_cpu)

def move_mouse(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(delay_cpu)

def click(amount=1, repeat=1):
    global bot_active
    for i in range(amount*repeat):
        if not bot_active:
            break
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0)
            time.sleep(0.001)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0)
        time.sleep(delay_click)

def click_here(x,y,amount=25):
    global bot_active
    if bot_active:
        move_mouse(x,y)
        click(amount)
    time.sleep(delay_cpu)
################# Game Functions ############################
def click_kiwi():
    click_here(945,620)
    time.sleep(delay_cpu)

def click_security():
    click_here(955,350)
    time.sleep(delay_cpu)

def click_target():
    click_here(1545,740, 10)
    time.sleep(delay_cpu)

def click_evil():
    click_here(1660,380,1)
    click_here(185,740,1)
    click_here(1370,420,1)
    click_here(1135,470,1)
    click_here(740, 860, 1)
    time.sleep(delay_cpu)

def click_upgrades():
    global upgrade_count
    if upgrade_count == 1: # Kiwi Bags
        click_here(250,580,1)
        click_here(440,500,1)
        click_here(600,485,1)
        print(f"Upgraded: Kiwi Bags")
    elif upgrade_count == 2: # Security
        click_here(725,535,1)
        click_here(1010,433,1)
        print(f"Upgraded: Security")
    elif upgrade_count == 3: # Kiwi Clicks
        click_here(960,925,1)
        click_here(1145,830,1)
        print(f"Upgraded: Kiwi Clicks")
    elif upgrade_count == 4: # Clicker Car
        click_here(1290,785,1)
        click_here(1285,680,1)
        print(f"Upgraded: Car")
    elif upgrade_count == 5: # Castle
        click_here(1790,520,1)
        click_here(1770,420,1)
        print(f"Upgraded: Castle")
        upgrade_count = 0
    upgrade_count +=1
    time.sleep(delay_cpu)

def archer_profession():
    global profession
    if profession == 0: # Start of a new Transcend.. Buys into the Archer profession
        click_here(1614, 946, 1) # Enter profression Tree
        click_here(490, 599, 1) # Buys into the Archer profession
    # elif profession > 1: # Buys only the minor nodes
    click_here(1614, 946, 1) # Enter profression Tree
    click_here(625, 631, 1) # 30% security
    click_here(553, 608, 1) # 30% security
    click_here(413, 616, 1) # 30% security
    click_here(358, 633, 1) # 30% security
    click_here(399, 686, 1) # 30% security
    click_here(312, 687, 1) # All Clicks Now Charge Security
# else: # Buys the Major nodes
    click_here(1614, 946, 1) # Enter profression Tree
    click_here(494, 761, 1) # Unlocks the Target
    click_here(454, 832, 1) # 50% target Multiplyer
    click_here(520, 837, 1) # 50% target Multiplyer
    click_here(582, 690, 1) # 30% security
    click_here(659, 687, 1) # Clicks shoot at King
    click_here(490, 599, 1) # 60% security
    click_here(496, 503, 1) # Security speed boosts Kiwis Clicks
    click_here(452, 560, 1) # Security speed boosts Bags
    click_here(534, 557, 1) # Security Speed boosts Coins
    click_here(1815,85, 1) # Exit Profession Tree -> Effects all if statements here as it's the last thing done for the whole process.
    profession += 1
    time.sleep(delay_cpu)

def click_king():
    for i in range(25):
        click_here(random.randint(1100, 1600), 350, 1)
    time.sleep(delay_cpu)

def click_transcend():
    click_here(325, 185, 1) # Opens Transcendant tree
    click_here(1750, 970, 1) # Clicks transcend
    click_here(812, 570, 1) # Confirms
    time.sleep(5.0) # Waits 5 seconds for the game to load
    click_here(1815, 80, 1) # Exits transcendant tree after transcending
    time.sleep(delay_cpu)

################ Main Bot Loop #############################
def bot_loop():
    global running
    global bot_active
    global profession
    
    # king = 0
    transcend = 0
    loop = 0
    while running:
        if bot_active == False:
            time.sleep(0.1)
        if bot_active:
            # Main Loop
            # for i in range(5):
            #     click_kiwi()
            #     click_security()
            #     click_target()
            # Every-So-Often clicks
            # click_upgrades()
            click_evil()
            # archer_profession()
            # click_king()
            
            # Conditionals
            if transcend >= 40:
                # click_transcend()
                # king = 0
                transcend = 0
                profession = 0
            
            # Build the Conditionals
            # king += 1
            transcend += 1
            loop += 1
            # print(f"        King = {king}")
            print(f"        Transcendance = {transcend}")
            print(f"        Profession = {profession}")
            print(f"        Loop = {loop}")
            # Sleep
            time.sleep(delay_cpu)
#############################################
def main():
    global running
    keyboard.add_hotkey(keybind_quit, quit_program)
    keyboard.add_hotkey(keybind_toggle_bot, toggle_bot)
    keyboard.add_hotkey(keybind_mouse_pos, get_mouse_pos)
    print(f""" 
✅ Program Running!
        Press {keybind_mouse_pos} to get the mouse pos.
        Press {keybind_toggle_bot} to toggle the bot.
        Press {keybind_quit} to quit the program!
        """)
    while running:
        bot_loop()
if __name__ == "__main__":
    main()







"""     Old Code

def click_here(x,y,amount=25):
    global bot_active
    if bot_active:
        move_mouse(x,y)
        click(amount)
    time.sleep(delay_cpu)




# GHOST CLICKS but the game doesn't recognize them :(
def click_here(x,y,amount=25):
    global bot_active
    if bot_active:
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if not hwnd:
                logging.error("Target window not found!")
                return
            
            lParam = win32api.MAKELONG(x, y)
            
            # This line is super important — many windows only respond to clicks on child controls
            hWnd1 = win32gui.FindWindowEx(hwnd, None, None, None)
            
            for i in range(amount):
                win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
                win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)
        
        except Exception as e:
            logging.error(f"Click failed: {e}")
        time.sleep(delay_cpu)

"""