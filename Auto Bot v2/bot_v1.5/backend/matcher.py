import  cv2
import numpy as np
from typing import Optional, Tuple

def find_template(screen: np.ndarray, template_path: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
    # Find template ins screen. Returns (x, y) center of match or None is not found.
    
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        return None
    
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    return None