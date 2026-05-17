# learning.py
import subprocess
from PIL import Image
import time
import cv2
import numpy as np
import io
import os


class BotController:
    def __init__(self):
        self.play_button = (500,500) # Coords for play ad button
        self.close_button = (500,500)
        self.ad_time = 60 # Seconds
        
    def load_templates(self, start_dir = "templates/ad_start", close_dir = "templates/ad_close"):
        templates = {"start":[], "close":[]}
        for filename in os.listdir(start_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                templates["start"].append(os.path.join(start_dir, filename))
        for filename in os.listdir(close_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                templates["close"].append(os.path.join(close_dir, filename))
        print(f"Loaded {len(templates['start'])} start tempolates and {len(templates['close'])} close templates")
        return templates
    
    
    # The "meat" of the program
    def run_adb(self, command: list[str]):
        # Prints the command we're about to run. 
        print("Running:", "adb", " ".join(command))
        # Run adb command safely
        result = subprocess.run(["adb"] + command, check=True)
        return result
    #
    
    
    # ADB Control Layers
    def tap(self, x,y):
        return self.run_adb(["shell", "input", "tap", str(x), str(y)])
    def swipe(self, x1, y1, x2, y2, duration):
        return self.run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
    def press_key(self, keycode):
        return self.run_adb(["shell", "input", "keyevent", str(keycode)])
    #
    
    
    # Adding "Vision"
    def get_screenshot(self, filename="screen.png"): # Saves and Reads with Disk Drive
        with open(filename, "wb") as f:
            subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
        img = Image.open(filename)
        img.show()
        return img
    def get_screencap(self): # Reads from RAM
        result = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout = subprocess.PIPE,
            check = True
        )
        return Image.open(io.BytesIO(result.stdout))
    #


    def find_image_on_screen(self, screen_img, template_path, threshold = 0.8):
        screen_cv = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2BGR)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            return max_loc # (x,y) where template matched
        return None
    
    
    # Logic Looping. Main bot program put together in one method.
    def watch_ad_cycle(self, templates, check_interval = 1, max_wait = 900):
        # Wait for ad to start
        start_time = time.time()
        while True:
            screen_img = self.get_screencap()
            found = False
            for start_template in templates["start"]:
                coords = self.find_image_on_screen(screen_img, start_template)
                if coords:
                    print(f"Ad detected with the template: {start_template}")
                    self.tap(coords[0], coords[1])
                    found = True
                    break
            if found:
                break
            elif time.time() - start_time > max_wait:
                print("Timeout: ad not detected")
                return
            else:
                print("Waiting for ad to appear...")
                time.sleep(check_interval)
        # Wait for close button to appear
        start_time = time.time()
        while True:
            screen_img = self.get_screencap()
            found = False
            for close_template in templates["close"]:
                coords = self.find_image_on_screen(screen_img, close_template)
                if coords:
                    self.tap(coords[0], coords[1])
                    print(f"Ad closed using template: {close_template}")
                    found = True
                    break
            if found:
                break
            elif time.time() - start_time > max_wait:
                print("Timeout: close button not detected")
                return
            else:
                print(f"Watching ad... waiting {check_interval} seconds for the close button.")
                time.sleep(check_interval)
    #
    
    
    # def navigation(self):
        
    #
    def run_main_loop(self,templates, categories, ad_button_coords, max_cycles):
        
    #



# End of program.
if __name__ == "__main__":
    bot = BotController()
    templates = bot.load_templates()
    bot.watch_ad_cycle(templates)
    
    categories = {
        "menu_1": (300, 1200),
        "menu_2": (5,5),
        "menu_3": (5,5),
    }  
    ad_button_coords = (5,5)
    bot.run_main_loop(templates, categories, ad_button_coords, max_cycles = 10)