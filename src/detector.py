import numpy as np
import cv2
import mss

class Detector:

    def __init__(self):
        self.location = [0, 0, 0]
    def scan(self):
        self.location = self.get_location()

    def get_location(self):
        return [0, 0, 0]