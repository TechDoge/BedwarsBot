from actions import Actions
from decisions import Decisions

class Player:

    def __init__(self):
        self.actions = Actions()
        self.decisions = Decisions()
        self.current_decision = []

    def act(self):
        self.current_decision = self.decisions.get_decision()

        for d in self.current_decision:
            header = d.split("-")[0]
            interaction = d.split("-")[1]
            if header == "hold":
                self.actions.hold_key(interaction)
            if header == "rel":
                self.actions.rel_key(interaction)
            if header == "click":
                if interaction == "left":
                    self.actions.left_click()
                if interaction == "right":
                    self.actions.right_click()
            if header == "move":
                x, y = interaction.split(",")
                self.actions.move_mouse(int(x), int(y))
