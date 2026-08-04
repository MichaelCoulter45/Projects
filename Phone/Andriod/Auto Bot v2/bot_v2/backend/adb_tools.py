# adb_tools.py
"""
Small helper module for talking to an Android device with ADB.

Provides:
 - get_screenshot_pil()  -> PIL.Image (RGB) or None
 - get_screenshot_cv2()  -> OpenCV BGR ndarray or None (faster)
 - save_screenshot(path) -> bool
 - tap(x, y)
 - swipe(x1,y1,x2,y2,duration_ms)
 - get_device_size()     -> (width, height) or None
 - is_device_connected() -> bool
"""
import subprocess # runs ADB commands
import io
from io import BytesIO # Let's us turn raw bytes returned by ADB into an in-memory file (not disk writting)
import re
from typing import Optional, Tuple

# image tools; provides both PIL and cv2 outputs ###
import numpy as np                                 #
import cv2                                         #
from PIL import Image                              #
#####                                           ####




# If ADB is not in path, then replace "adb" with the full path to adb.exe
ADB_PATH = "adb"
# Default timeout for adb commands (seconds). Prevents the script from hanging indefinitely.
ADB_TIMEOUT = 8





def _run_adb(args, timeout=ADB_TIMEOUT):
    """
    Internal helper that  runs: [ADB_PATH] + args
    Returns subprocess.CompletedProcess or None on timeout.
    """
    cmd = [ADB_PATH] + list(args)
    try:
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return cp
    except FileNotFoundError:
        raise RuntimeError
    except subprocess.TimeoutExpired:
        # Timeout - caller can choose to retry
        return None

def is_device_connected() -> bool:
    # Return True if at least one device is listed as 'device' by 'adb devices'
    cp = _run_adb(["devices"])
    if cp is None or cp.returncode != 0:
        return False
    out = cp.stdout.decode(errors="ignore")
    # Skip header line; look for lines like: <serial>\tdevice
    for line in out.splitlines()[1:]:
        if "\tdevice" in line:
            return True
    return False

def get_screenshot_pil(timeout=ADB_TIMEOUT) -> Optional[Image.Image]:
    """
    Capture a screenshot via 'adb exec-out screencap -p' and return a PIL.Image (RBG).
    Uses BytesIO; no file I/O.
    """
    cp = _run_adb(["exec-out", "screencap", "-p"], timeout=timeout)
    if cp is None or cp.returncode != 0:
        return None
    data = cp.stdout
    try:
        img = Image.open(BytesIO(data))
        return img.convert("RBG")
    except Exception:
        # Fallback: decode with OpenCV then convert to PIL
        nparr = np.frombuffer(data, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # RBG
        if img_cv is None:
            return None
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_cv)

def get_screenshot_cv2(timeout=ADB_TIMEOUT) -> Optional[np.ndarray]:
    """
    Capture screen and return a cv2 image (BGR ndarray).
    This is slightly faster than PIL path because it decodes directly with OpenCV.
    """
    cp = _run_adb(["exec-out", "screencap", "-p"], timeout=timeout)
    if cp is None or cp.returncode != 0:
        return None
    data = cp.stdout
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # RGB
    return img # May be NONE on failure

def save_screenshot(path: str, timeout=ADB_TIMEOUT) -> bool:
    # Save a screenshot to disk (useful for capturing templates). Returns True on success.
    img = get_screenshot_pil(timeout=timeout)
    if img is None:
        return False
    img.save(path)
    return True

def tap(x: int, y: int, timeout=ADB_TIMEOUT) -> bool:
    # Send a tap event to the device. Returns True if the adb command succeeded.
    cp = _run_adb(["shell", "input", "tap", str(int(x)), str(int(y))], timeout=timeout)
    return (cp is not None and cp.returncode == 0)

def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300, timeout=ADB_TIMEOUT) -> bool:
    # Sends a swipe to the device. duration_ms is in milliseconds.
    cp = _run_adb(["shell", "input", "swipe",
                str(int(x1)), str(int(y1)), str(int(x2)),
                str(int(y2)), str(int(duration_ms))], 
                timeout=timeout)
    return (cp is not None and cp.returncode == 0)

def get_device_size() -> Optional[Tuple[int, int]]:
    # Return (width, height) from 'adb shell wm size' or None on failure.
    cp = _run_adb(["shell", "wm", "size"])
    if cp is None or cp.returncode != 0:
        print("[!] Failed to run the adb command.")
        return None
    # Check if adb command failed
    if cp.returncode != 0:
        stderr = cp.stderr.decode(errors="ignore") if cp.stderr else ""
        if "unauthorized" in stderr.lower():
            print("[!] Device unauthorized. Please check your phone for USB debugging authorization prompt.")
        else:
            print(f"[!] adb command failed: {stderr.strip()}")
        return None
    out = cp.stdout.decode(errors="ignore")
    m = re.search(r'(\d+)[xX](\d+)', out)
    if m:
        return int(m.group(1)), int(m.group(2))
    print("[!] Could not parse device size from adb output.")
    return None

def screencap() -> Optional[Image.Image]:
    """
    Capture the current screen of the connected device.
    Returns a PIL Image on success or None on failure.
    """
    try:
        # Run adb screencap to stdout
        cp = subprocess.run(
            ["adb", "exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout = 5
        )
        if cp.returncode != 0:
            print(f"[adb_tools] screencap failed: {cp.stderr.decode(errors='ignore')}")
            return None
        
        # Convert binary PNG to PIL Image
        img_data = cp.stdout
        img = Image.open(io.BytesIO(img_data))
        return img
    
    except subprocess.TimeoutExpired:
        print("[adb_tools] screencap timed out.")
        return None
    except Exception as e:
        print(f"[adb_tools] screencap error: {e}")
        return None

def screenshot():
    screencap()

