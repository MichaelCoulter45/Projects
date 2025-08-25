from backend import adb_tools
from backend import matcher


def testing():
    print("Device size:", adb_tools.get_device_size())
    #
    img = adb_tools.get_screenshot()
    if img is not None:
        print("Screenshot shape:", img.shape)
        adb_tools.tap(1400, 20)  # test tap
    else:
        print("No screenshot!")

def matching():
    img = adb_tools.get_screenshot()
    if img is not None:
        pos = matcher.find_template(img, "templates/upgrade.png", threshold = 0.85)
        if pos:
            print(f"Found template at {pos}")
            adb_tools.tap(*pos)
        else:
            print("No match found.")

def main():
    #matching()
    adb_tools.save_screenshot()



main()