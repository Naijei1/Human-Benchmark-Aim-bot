import cv2
import numpy as np
from mss import mss
from pathlib import Path
import sys
import pyautogui
import imutils

import mss.tools

pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0
class visionClass:
    
    confidence = 0.8
    scapture = None
    
    def __init__(self, confidence=0.8):
        self.scapture = mss.mss()
        self.confidence = confidence

    def load_asset_grayscale(self, filepath):
        """
        Loads the reference .png from disk.
        Crucial: Must handle FileNotFoundError.
        """
        try:
            img_arry = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
            # cv2.imshow("Image", img_arry)
            # cv2.waitKey(0)
            return img_arry
        except:
            print("Invalid asset file path, exiting program...")
            sys.exit()
        
    def scan_region(self, template_img, region=None):
        """
        Scans screen and returns coords for found template
        """
        if region is None:
            monitor = self.scapture.monitors[1]
            screen = np.array(self.scapture.grab(monitor))
            off_x, off_y = 0, 0
        else:
            if isinstance(region, tuple):
                region = {
                    "left": int(region[0]),
                    "top": int(region[1]),
                    "width": int(region[2]),
                    "height": int(region[3])
                }
            
            screen = np.array(self.scapture.grab(region))
            off_x = region['left']
            off_y = region['top']
        
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
        
        current_scale = getattr(self, 'cached_scale', None)
        
        if current_scale is not None:
            resized_template = imutils.resize(template_img, width=int(template_img.shape[1] * current_scale))
            
            if resized_template.shape[0] <= screen_gray.shape[0] and resized_template.shape[1] <= screen_gray.shape[1]:
                res = cv2.matchTemplate(screen_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(res)
                
                if maxVal >= self.confidence:
                    return self._calculate_coords(maxLoc, template_img, current_scale, off_x, off_y)
            
            self.cached_scale = None

        found = None
        for scale in np.linspace(0.5, 2.0, 1): 
            resized_template = imutils.resize(template_img, width=int(template_img.shape[1] * scale))
            
            if resized_template.shape[0] > screen_gray.shape[0] or resized_template.shape[1] > screen_gray.shape[1]:
                continue

            result = cv2.matchTemplate(screen_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            if maxVal > 0.9:
                found = (maxVal, maxLoc, scale)
                break

            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, scale)

        if found:
            (best_score, best_loc, best_scale) = found
            if best_score >= self.confidence:
                self.cached_scale = best_scale
                return self._calculate_coords(best_loc, template_img, best_scale, off_x, off_y)
        
        return None

    def _calculate_coords(self, loc, template, scale, off_x, off_y):
        """Helper to keep the main logic clean"""
        h, w = template.shape
        actual_w = int(w * scale)
        actual_h = int(h * scale)
        
        center_x = loc[0] + (actual_w // 2) + off_x
        center_y = loc[1] + (actual_h // 2) + off_y
        return (center_x, center_y)
            
if __name__ == "__main__":
    try:
        clicks = 0
        vision = visionClass(0.8)
        img = vision.load_asset_grayscale("/Users/naijei/ML-Bots/Vision-Controller/target.png")
        while True:
            res = vision.scan_region(img, (350, 155, 1050, 549)) #EDIT REGION IF OUT OF BOUNDS
            if res != None:
                clicks += 1
                pyautogui.click(res, _pause=False)
                if(clicks > 30):
                    break
    except:
        print("Program Exited")