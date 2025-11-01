# match_verify.py
import cv2
import numpy as np
import os
import time
import pyautogui

# ---------- CONFIG ----------
SCALE = 0.5                # downscale frames for matching speed, adjust
THRESH_TEMPLATE = 0.55     # template match threshold (on resized frame)
ORB_MATCH_THRESHOLD = 8    # min number of good ORB matches to accept
EDGE_DENSITY_MIN = 0.05    # min edge density (alive slimes tend to have structure)
EDGE_DENSITY_MAX = 0.5     # max edge density (avoid extremely noisy regions)
NEGATIVE_CORRELATION = 0.90 # if puddle correlates above this, reject
# ----------------------------

orb = cv2.ORB_create(500)

def load_templates_with_orb(dir_path, scale=SCALE):
    """
    Loads grayscale templates, stores original size and ORB keypoints/descriptors.
    Returns list of dicts: {name, img, img_small, kps, desc, h, w}
    """
    templates = []
    for fname in sorted(os.listdir(dir_path)):
        path = os.path.join(dir_path, fname)
        if not os.path.isfile(path):
            continue
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        h, w = img.shape[:2]
        small = cv2.resize(img, (int(w * scale), int(h * scale)))
        kps, desc = orb.detectAndCompute(img, None)  # note: use original-resolution descriptors
        templates.append({
            "name": fname,
            "img": img,
            "img_small": small,
            "kps": kps,
            "desc": desc,
            "h": h, "w": w
        })
    return templates

def edge_density(img_gray):
    """Return proportion of edge pixels in image region (0..1)."""
    edges = cv2.Canny(img_gray, 50, 150)
    return (edges > 0).sum() / (img_gray.shape[0] * img_gray.shape[1] + 1e-9)

# simple ORB verify: count good matches with Lowe ratio test
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
def orb_verify(template_desc, roi_gray):
    if template_desc is None or len(template_desc) == 0:
        return 0
    # compute ORB on ROI at original template scale (resize roi to template size if needed)
    # ROI should be approx same scale as template; if not, we compute on roi resized to template size:
    try:
        kp2, desc2 = orb.detectAndCompute(roi_gray, None)
    except Exception:
        return 0
    if desc2 is None:
        return 0
    # knn match and ratio test
    matches = bf.knnMatch(template_desc, desc2, k=2)
    good = 0
    for m_n in matches:
        if len(m_n) < 2:
            continue
        m, n = m_n
        if m.distance < 0.75 * n.distance:
            good += 1
    return good

# main verify function: takes frame_gray (resized) and the best candidate location & template
def verify_and_click(
    frame_full_bgr,
    frame_resized_gray,
    best_template,
    best_loc,
    left,
    top,
    scale=SCALE,
    negative_templates=None,
    force_click=False,
    debug_visual=False,  # 👈 optional visualization toggle
):
    x_res, y_res = best_loc
    t_h, t_w = best_template["img_small"].shape[:2]

    # Convert to original frame coords
    x_full = int(x_res / scale)
    y_full = int(y_res / scale)
    t_w_full = int(t_w / scale)
    t_h_full = int(t_h / scale)

    # Clamp ROI
    H, W = frame_full_bgr.shape[:2]
    x0 = max(0, x_full); y0 = max(0, y_full)
    x1 = min(W, x_full + t_w_full); y1 = min(H, y_full + t_h_full)
    roi_full = frame_full_bgr[y0:y1, x0:x1]
    if roi_full.size == 0:
        print("⚠️ Empty ROI — skipping.")
        return False

    roi_gray_full = cv2.cvtColor(roi_full, cv2.COLOR_BGR2GRAY)

    # Skip checks if forcing
    if not force_click:
        # Edge density test (slightly relaxed)
        ed = edge_density(roi_gray_full)
        if ed < (EDGE_DENSITY_MIN * 0.5) or ed > (EDGE_DENSITY_MAX * 1.5):
            print(f"Verification fail: edge_density={ed:.3f} (outside range)")
            return False

        # ORB verify — lowered threshold and added scoring printout
        good_matches = orb_verify(best_template["desc"], roi_gray_full)
        print(f"Verification: {best_template['name']} | ORB good={good_matches} | Edge={ed:.3f}")
        if good_matches < (ORB_MATCH_THRESHOLD * 0.75):
            print(f"Verification fail: only {good_matches} good matches (< {ORB_MATCH_THRESHOLD * 0.75})")
            return False

        # Negative template rejection (still strict)
        if negative_templates:
            for neg in negative_templates:
                neg_small = cv2.resize(neg["img"], (roi_gray_full.shape[1], roi_gray_full.shape[0]))
                res = cv2.matchTemplate(roi_gray_full, neg_small, cv2.TM_CCOEFF_NORMED)
                _, mv, _, _ = cv2.minMaxLoc(res)
                if mv >= NEGATIVE_CORRELATION:
                    print(f"Verification fail: matched puddle [{neg['name']}] with corr={mv:.2f}")
                    return False
    else:
        print(f"💥💥💥 Force clicking [{best_template['name']}] — skipping verification checks.")
        # mark as forced for logging
        good_matches = "FORCED"
        ed = "FORCED"


    # Passed checks OR force click
    click_x = x_full + (x1 - x0)//2 + left
    click_y = y_full + (y1 - y0)//2 + top

    # Optional: draw visual debug rectangle on screen frame
    if debug_visual:
        cv2.rectangle(frame_full_bgr, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.imshow("Verification ROI", frame_full_bgr)
        cv2.waitKey(1)

    # Simulate click
    mx, my = pyautogui.position()
    pyautogui.click(click_x, click_y)
    pyautogui.moveTo(mx, my)

    print(f"✅ Verification PASSED for [{best_template['name']}] | ORB={good_matches} | Edge={ed}")
    return True

# ---------------- Example usage inside your main loop ----------------
# (This pseudocode shows how to call the pipeline from your main dxcam loop)
#
# left,top = region offset (DXCam region left/top)
# frame_full = cam.get_latest_frame()   # full-region frame (already the game window)
# frame_small = cv2.resize(frame_full, (0,0), fx=SCALE, fy=SCALE)
# frame_small_gray = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
#
# # fast search: find best match among preloaded small templates
# best_score = -1; best_template = None; best_loc = None
# for tpl in live_templates_small:
#     res = cv2.matchTemplate(frame_small_gray, tpl["img_small"], cv2.TM_CCOEFF_NORMED)
#     _, mv, _, ml = cv2.minMaxLoc(res)
#     if mv > best_score:
#         best_score = mv; best_template = tpl; best_loc = ml
#
# if best_score >= THRESH_TEMPLATE:
#     ok = verify_and_click(frame_full, frame_small_gray, best_template, best_loc,
#                           left, top, scale=SCALE, negative_templates=dead_templates)
#     if ok:
#         print("Clicked verified live template:", best_template["name"])
#     else:
#         print("Candidate failed verification (likely puddle or false match)")
#
# ---------------------------------------------------------------------
