from detector import Detector

class Decisions:
    
    def __init__(self):
        self.detector = Detector(0, 0, 1920, 1080)
        self.current_shot = None

    def get_decision(self):
        self.current_shot = self.detector.get_shot()