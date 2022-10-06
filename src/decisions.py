from detector import Detector

class Decisions:
    
    def __init__(self):
        self.detector = Detector()

    def get_decision(self):
        self.detector.scan()