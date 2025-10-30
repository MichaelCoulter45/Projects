import cv2
import numpy as np
from typing import Optional, Tuple


def match_template(screen_img: np.ndarray, template_path: str, threshold: float = 0.90) -> Optional[Tuple[int, int]]:
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"⚠️ Could not load template {template_path}")
        return None
    
    # Convert to grayscale
    gray_screen = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    
    # Match template
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        # Computing the center of the match
        t_h, t_w = template.shape[:2]
        center_x = max_loc[0] + t_w // 2
        center_y = max_loc[1] + t_h // 2
        print(f"[Match] {template_path} at ({center_x}, {center_y} with {max_val:.2f})")
        return (center_x, center_y)
    else:
        return None