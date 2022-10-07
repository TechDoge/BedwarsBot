from detector import Detector

class Decisions:

    def __init__(self):
        self.detector = Detector(0, 0, 1920, 1080)
        self.current_shot = None
        self.current_location = None

    def get_decision(self):
        self.detector.scan()
        self.current_shot = self.detector.shot
        self.current_location = self.detector.location