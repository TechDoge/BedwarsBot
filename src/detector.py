import numpy as np
import cv2
import mss

class Detector:

    def __init__(self, window_x, window_y, window_width, window_height):
        self.x = window_x
        self.y = window_y
        self.width = window_width
        self.height = window_height

    def get_shot(self):
        with mss.mss() as sct:
            monitor = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            img_array = np.array(sct.grab(monitor))
            return img_array