# TreasureChestClicker.py
import sys
import time
import threading
import keyboard
import win32api
import win32con
import pyautogui


# Goals:
""" 
X - auto click chest..
X - check if chest is dying at a certain pace.
X    -> Don't upgrade and save up for next chest. Pixel check behind chest..? Pixel at healthbar.
X - auto click passive upgrade (TBH no template needed, just coords...)
X - auto click the 4 items to use (exp, dmg, coins, money)
X - Auto upgrade equipped cursor
X - swipe and click bottom of screen to sweep any artifacts
X - Set a target skill point goal to check if we're set to prestiege.
X - Add in a GUI
X - Check potion quantity to check if need to buy more.
X * Automate the prestiege process? Like, loop gameplay to prestieges?
X    -> Check if skill points is a certain value and proceed to prestiege..?
X * auto click new cursor?? - Maybe...
X    -> Need a list of which cursors to click for idle bonus

- Intead of matching templates to click immediately, This one can be a 'checklist' system.
    -> Where we process each template in order and do a series of checks to have the bot
        process through the game naturally. Unlike Slime Squisher where we were clicking
        on slimes immediately. This will automate the game processes since it already does
        the bulk of the work with the passive damage to the chest.

"""
##################
TEMPLATES_DIR = r"C:\Users\power\git\Projects\Game Bots\PC\TreasureChestClicker\templates"
ITEMS_DIR = r"C:\Users\power\git\Projects\Game Bots\PC\TreasureChestClicker\templates\items"
CLICKABLES_DIR = r"C:\Users\power\git\Projects\Game Bots\PC\TreasureChestClicker\templates\clickables"
WIN_TITLE = "TreasuerChestClicker"

SCREEN_REGION = (0, 50, 1280, 720)
LEFT, TOP, W, H = SCREEN_REGION
MIDDLE_POINT = ((W/2), (H/2))           # ((1280/2), (720/2))
# -- Screen Zones -- #
# ZONE_HALF_UPPER = (0, MIDDLE_POINT[1])     # From 0 to the middle horizonally
# ZONE_HALF_LOWWER = (MIDDLE_POINT[1], H)   # From the middle horizontal to the whole end
# ZONE_HALF_LEFT = (0, MIDDLE_POINT[0])   # From 0 to the middle vertically
# ZONE_HALF_RIGHT = (MIDDLE_POINT[0], W)  # From the middle vertically to the whole height

KEY_TOGGLE_BOT = "."
KEY_PRINT_MOUSE_POS = "/"
KEY_QUIT_PROGRAM = "Q"

DELAY_CPU = 0.01
DELAY_CLICK = 0.03

# -- Template Matching -- #
MATCH_THRESHOLD = 0.75
DXCAM_FPS = 30
###

last_mouse_pos = None
current_mouse_pos = None

new_prestiege = None
running = True
bot_active = False
mouse_pos_active = False

mouse_pos_max_x = W
mouse_pos_max_y = H

####### -- Functions -- #######
def load_templates():
    
    
    time.sleep(DELAY_CPU)
    pass


def scroll_up(repeat=1):
    x,y = pyautogui.position()
    for i in range(repeat):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,120)
    time.sleep(1)
    # print("Scrolling UP")
    return True
def scroll_down(repeat=1):
    x,y = pyautogui.position()
    for i in range(repeat):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,x,y,-120)
    time.sleep(1)
    # print("Scrolling DOWN")
    return True


def toggle_bot():
    global bot_active
    bot_active = not bot_active
    print("✅ Bot activated!" if bot_active else "⏸️ PAUSING...")
    return True


def toggle_mouse_pos():
    global mouse_pos_active
    mouse_pos_active = not mouse_pos_active
    return True


def click(x:int,y:int,repeat=1):
    for i in range(repeat):
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0,0)
        time.sleep(0.001)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0,0)
    time.sleep(DELAY_CLICK)
    return True


def print_mouse_pos():
    print(pyautogui.position())





def quit_program():
    global running
    running = False
    print("🛑 Quitting...")
    sys.exit(0)
####### -- Game Loop Functions -- ########
def buy_max_passive_level():
    click(830, 640)
    click(820, 590)
    click(880, 590)
    time.sleep(DELAY_CPU)
    return True


def use_items():
    click(280, 250) # Clicks the items tab
    click(180, 390, 4)
    click(70, 400, 4)
    click(70, 500, 4)
    click(180, 500, 4)
    click(70, 700, 4)
    click(180, 700, 4)
    click(180, 600, 4)
    scroll_down(20)
    click(180, 570, 4)
    click(70, 580, 4)
    click(70, 680, 4)
    scroll_up(20)
    time.sleep(DELAY_CPU)
    return True


def buy_items():
    x, y = 1100, 290
    click(980, 300) # items tab
    win32api.SetCursorPos((1100,290))
    scroll_up(100)
    for i in range(2):
        for j in range(8):
            click(x,y)
            y += 58
        scroll_down(40)
        y = 261
    time.sleep(DELAY_CPU)
    return True


def sweep_bottom(x1=400,x2=900,y=680, repeat=2):
    while x1 < x2:
        click(x1,y)
        x1 += 20
    time.sleep(DELAY_CPU)


def upgrade_cursors():
    click(980, 245) # cursor tab
    win32api.SetCursorPos((1230,345))
    scroll_up(100)
    click(1230, 345)
    click(1230, 460)
    click(1230, 585)
    click(1230, 695)
    scroll_down(36)
    click(1230, 355)
    click(1230, 470)
    click(1230, 710)
    scroll_down(36)
    click(1230, 490)
    click(1230, 545)
    click(1230, 730)
    # time.sleep(DELAY_CPU)
    return True


def upgrade_all_items():
    x, y = 1230, 290
    click(980, 300) # items tab
    win32api.SetCursorPos((1230,290))
    scroll_up(100)
    for i in range(2):
        for j in range(8):
            click(x,y)
            y += 58
        scroll_down(40)
        y = 261
    time.sleep(DELAY_CPU)
    return True


def check_for_prestiege():
    
    
    time.sleep(DELAY_CPU)
    pass


def fresh_prestiege():
    
    
    time.sleep(DELAY_CPU)
    pass


def bot_loop():
    global bot_active
    count = 0
    while running:
        if not bot_active:
            time.sleep(DELAY_CPU)
            continue
        
        
        buy_max_passive_level()
        use_items()
        sweep_bottom()
        buy_items()
        # upgrade_cursors()
        upgrade_all_items()
        
        
        count += 1
        print(f"{count}")
        time.sleep(DELAY_CPU)
def main():
    keyboard.add_hotkey(KEY_TOGGLE_BOT, toggle_bot)
    keyboard.add_hotkey(KEY_PRINT_MOUSE_POS, print_mouse_pos)
    keyboard.add_hotkey(KEY_QUIT_PROGRAM, quit_program)
    
    worker = threading.Thread(target=bot_loop, daemon=True)
    worker.start()
    
    print(f"""
        Press [{KEY_TOGGLE_BOT}] to toggle the bot!
        Press [{KEY_PRINT_MOUSE_POS}] to print mouse position!
        Press [{KEY_QUIT_PROGRAM}] to quit the program!
        """)
    while running:
        time.sleep(DELAY_CPU)


if __name__ == "__main__":
    main()