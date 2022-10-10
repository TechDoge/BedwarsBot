from detector import Detector
import time
from data.action_tables import tables

class ProcessDecider:

    def __init__(self):
        self.action_set = ["collect_gen", "buy_defense", "build_defense"]
        self.current = self.action_set[0]

    def get_current_table(self):
        return tables[self.current]

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
        self.action_table = ActionTable(self.processer.get_current_table(), time.time())
        self.time_since_last_process = time.time()

    def get_decision(self):
        self.detector.scan()
        self.current_shot = self.detector.shot
        self.current_location = self.detector.location
        self.resources = self.detector.resources
        action = self.action_table.get_moves()

        return action
        