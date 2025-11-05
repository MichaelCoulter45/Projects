# template_tool.py
# pyinstaller --noconfirm --clean --noconsole --onefile template_tool.py
import cv2
import pyautogui
import os
import numpy as np
import time
import win32gui

# Directory to save templates
TEMPLATE_DIR = r"C:\Users\power\git\Projects\Game Bots\PC\Slime Squisher\templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)

window_name = "Slime Squisher"  # your game window

def get_window_bbox(window_name):
    import win32gui
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        return win32gui.GetWindowRect(hwnd)
    else:
        raise Exception(f"Window '{window_name}' not found!")

def capture_template(name="template", padding=5):
    left, top, right, bottom = get_window_bbox(window_name)
    print(f"Bounding window region: {left}, {top}, {right}, {bottom}")

    while True:
        # Screenshot of the game window
        screen = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

        # Display the screenshot
        cv2.imshow("Template Capture", frame)
        key = cv2.waitKey(1) & 0xFF

        # Press 'c' to select a template area
        if key == ord('c'):
            print("Click and drag a rectangle on the window to select the template.")

            # Select ROI interactively
            roi = cv2.selectROI("Template Capture", frame, showCrosshair=True, fromCenter=False)
            x, y, w, h = roi
            if w > 0 and h > 0:
                cropped = frame[y-padding:y+h+padding, x-padding:x+w+padding]
                filename = f"{name}_{int(time.time())}.png"
                path = os.path.join(TEMPLATE_DIR, filename)
                cv2.imwrite(path, cropped)
                print(f"Saved template: {path}")

        # Exit helper
        if key == ord('q'):
            print("Exiting template capture helper...")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Press 'c' to capture a template, 'q' to quit.")
    capture_template()
