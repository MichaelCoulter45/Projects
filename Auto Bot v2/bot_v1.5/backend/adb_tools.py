import subprocess
import cv2
import numpy as np
from typing import Optional, Tuple

def _run_adb(args: list, timeout: float = 5.0) -> Optional[subprocess.CompletedProcess]:
    # Run adb command and return CompletedProcess or None on failure.
    try:
        return subprocess.run(
            ["adb"] + args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            timeout=timeout
        )
    except Exception:
        return None

def get_device_size() -> Optional[Tuple[int, int]]:
    # Return (width, height) from 'adb shell wm size' or None on failure.
    cp = _run_adb(["shell", "wm", "size"])
    if not cp or cp.returncode != 0:
        return None
    out = cp.stdout.decode(errors = "ignore")
    import re
    m = re.search(r'(\d+)[xX](\d+)', out)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None

def get_screenshot() -> Optional[np.ndarray]:
    # Capture a screenshot from the device and return as a OpenCV image (BGR).
    cp = _run_adb(["exec-out", "screencap", "-p"])
    if not cp or cp.returncode != 0:
        return None
    data = cp.stdout
    img_array = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def save_screenshot(path: str = "screenshot.png") -> bool:
    # Saves a screenshot of the device to computer.
    img = get_screenshot()
    if img is None:
        return False
    cv2.imwrite(path, img)
    return True

def tap(x: int, y: int) -> bool:
    # Send a tap to (x, y) on the device
    cp = _run_adb(["shell", "input", "tap", str(x), str(y)])
    return cp is not None and cp.returncode == 0