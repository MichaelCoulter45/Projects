import subprocess, os
import cv2
import numpy as np

ADB = r"C:\platform-tools\adb.exe"
TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)


""" 
For Bluestacks:
adb connect 127.0.0.1:5555
"""


def screenshot():
    png = subprocess.check_output([ADB, "exec-out", "screencap", "-p"])
    return cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)

def main():
    while True:
        name = input("Template name (blank to quit): ").strip()
        if not name:
            break
        screen = screenshot()
        cv2.namedWindow("Select template", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Select template", 540, 960)
        # Drag a box, press ENTER/SPACE to confirm, C to cancel
        x, y, w, h = cv2.selectROI("Select template", screen, showCrosshair=False)
        cv2.destroyAllWindows()
        if w == 0 or h == 0: # Selected nothing
            print("Cancelled.")
            continue
        crop = screen[y:y+h, x:x+w]
        path = os.path.join(TEMPLATE_DIR, f"{name}.png")
        cv2.imwrite(path, crop)
        print(f"Saved {path} ({w}x{h})")

if __name__ == "__main__":
    main()
