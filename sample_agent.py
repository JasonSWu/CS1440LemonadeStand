from agent import Agent
from lemonade_result import LemonadeResult


class StickAgent(Agent):
    def __init__(self, loc):
        super().__init__()
        self.name = 'StickAgent'
        self.loc = loc

    def get_action(self):
        return self.loc

    def update(self, result: LemonadeResult):
        pass
