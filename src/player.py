from actions import Actions
from decisions import Decisions

class Player:

    def __init__(self):
        self.actions = Actions()
        self.decisions = Decisions()

    def act(self):
        decision = self.decisions.get_decision()