from typing_extensions import Self
from detector import Detector
import time
from data.action_tables import tables


default_player_info = {
    "location": [0, 0, 0],
    "resources": [0, 0, 0, 0]
}

class ProcessDecider:

    def __init__(self):
        self.current = "none"
        self.player_info = None

    def finished_start_collect_gen(self):
        if self.player_info["resources"][1] >= 4:
            return True 
        return False

    def decide_state(self):
        if (self.current == "none"):
            return "start_collect_gen"

        if (self.current == "start_collect_gen" and self.finished_start_collect_gen()):
            return "start_defend_bed"

        return "none"

    def get_current_table(self, info):
        self.player_info = dict(info)
        result = self.decide_state()
        if result != "none":
            self.current = result
            return tables[result]
        return result

class ActionTable:

    def __init__(self, table, init_time):
        self.init_time = init_time
        self.table = table

    def get_moves(self):
        result = []
        for move in self.table:
            if not move[2]:
                if time.time()-self.init_time >= move[1]:
                    result.append(move[0])
                    move[2] = True
        return result

class Decisions:

    def __init__(self):
        self.detector = Detector(0, 0, 1920, 1080)
        self.current_shot = None
        self.current_location = None
        self.processer = ProcessDecider()
        self.action_table = None

    def get_decision(self):
        self.detector.scan()
        self.current_shot = self.detector.shot
        self.current_location = self.detector.location
        self.resources = self.detector.resources
        self.player_info = {
            "location": self.current_location,
            "resources": self.resources
        }
        result_table = self.processer.get_current_table(self.player_info)
        if result_table != "none":
            self.action_table = ActionTable(result_table, time.time())
        action = self.action_table.get_moves()
        return action
        