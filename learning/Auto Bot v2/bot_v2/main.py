from backend import adb_tools
from backend import rules
from backend import rules
from rules import Rule, RuleManager
from rules_helpers import match_template_factory, tap_action  # we’ll build these next
import cv2
import subprocess
import numpy as np
import time



DEBUG_MODE = True
rules = RuleManager()

# Example rule
rules.add_rule(Rule(
    "Ad Ready",
    matcher=match_template_factory("templates/ad_ready.png"),
    action=tap_action,
    cooldown=5.0
))


################## Debug Zone: ##################
def debug():
    if DEBUG_MODE == True:
        # Tests to see if _run_adb() can reach the phone by getting the phone's screen size.
        # result = adb_tools._run_adb(["shell", "wm", "size"])
        # print(result)
        # if result:
        #     print(result.stdout.decode(errors="ignore"))
        # ##################
        # w,h = adb_tools.get_device_size()
        # print("Device is", w, "x", h)
        # ##################
        # print("ADB connected?", adb_tools.is_device_connected())
        # ok = adb_tools.save_screenshot("temp.png")
        # print("Saved?", ok)
        # ##################
        # tap_x, tap_y = 800, 1600
        # adb_tools.tap (tap_x, tap_y)
        # ##################
        # img = adb_tools.screencap()
        # if img:
        #     img.show() # opens in your default image viewer
        # else:
        #     print("Failed to capture screen.")
        ##################
        def live_preview(fps: int = 15): # This current setup only updates every 2 seconds - 0.5 fps. Still figuring out why.
            delay = 1.0 / fps # frame time budget
            screen_h = 1080 # Display Monitor height 1080p

            while True:
                start = time.time()
                img = adb_tools.screencap()
                if img is None:
                    print("⚠️ Failed to grab screenshot")
                    break
                
                # Convert PIL -> OpenCV format
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                # Resizing display window
                scale =  screen_h/ frame.shape[0]
                frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
                
                
                cv2.imshow("Phone Live Preview", frame)
                
                # Exit on 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # FPS Limiting
                elapsed = time.time() - start
                if elapsed < delay:
                    time.sleep(delay - elapsed)
                    
            cv2.destroyAllWindows()

def main():
    





# Main loop
while True:
    frame = adb_tools.get_screenshot_cv2()
    rules.run_rules(frame)