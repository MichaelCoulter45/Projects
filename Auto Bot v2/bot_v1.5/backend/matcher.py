import  cv2
import numpy as np
from typing import Optional, Tuple

def match_template(screen_img: np.ndarray, template_path: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
    """
    Match a template on the screen and return the (x, y) center of the best match if above threshold.
    :param screen_img: Screenshot as a numpy array (BGR format from OpenCV).
    :param template_path: Path to the template .png file.
    :param threshold: Minimum confidence [0.0–1.0].
    :return: (x, y) or None if no match found.
    """    
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"⚠️ Could not load template {template_path}")
        return None
    
    # Convert to Grayscale
    gray_screen = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
    
    # Match Template
    res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        # Compuiting the center of the match
        t_h, t_w = template.shape[:2]
        center_x = max_loc[0] + t_w // 2
        center_y = max_loc[1] + t_h // 2
        print(f"[Match] {template_path} at ({center_x}, {center_y}) with {max_val:.2f}")
        return (center_x, center_y)
    else:
        return None
