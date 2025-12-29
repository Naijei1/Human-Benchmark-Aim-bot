import cv2
import numpy as np
import mss
from pathlib import Path

class CardDetector:
    
    def __init__(self, confidence=0.8):
        # TODO: Initialize mss (screen capture)
        # TODO: Set confidence threshold
        pass

    def _preprocess(self, image):
        """
        Internal ETL: Converts raw BGRA screen capture to Grayscale.
        Input: Raw pixels (numpy array)
        Output: Gray pixels (numpy array)
        """
        pass

    def load_asset(self, filepath):
        """
        Loads the reference .png from disk.
        Crucial: Must handle FileNotFoundError.
        """
        pass

    def scan_region(self, template_img, region=None):
        """
        The Core Vision Logic.
        1. Grab screen (ROI or Full).
        2. Run cv2.matchTemplate.
        3. Filter results by 'confidence'.
        4. Return (x, y) coordinates or None.
        """
        pass

# --- Interface Execution ---
if __name__ == "__main__":
    # 1. Define ROI (Region of Interest)
    # HAND_REGION = {'top': x, 'left': y, 'width': w, 'height': h}
    
    # 2. Load Detector
    # bot = CardDetector()
    
    # 3. Trigger Search
    # print(bot.scan_region(template, HAND_REGION))
    pass