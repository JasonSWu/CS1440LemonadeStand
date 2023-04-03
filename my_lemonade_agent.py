from agent import Agent
from lemonade_result import LemonadeResult
import random


class LemonadeAgent(Agent):
    def __init__(self):
        # TODO: Name agent and implement any additional class characteristics you may need
        super().__init__()
        self.name = 'EnterNameHere'

    def get_action(self):
        # TODO: Enter logic to pick next result here
        try:
            last_opp_1 = self.opponent_1_actions[-1]
            last_opp_2 = self.opponent_2_actions[-1]
            action = (last_opp_1 + 6) % 12
        except:
            action = random.choice([2])
        return action

    def update(self, result: LemonadeResult):
        # TODO: Enter any logic you'd like to include in the update. Please check the base class update_actions before
        #  changing this
        pass


class RandomAgent(LemonadeAgent):
    def __init__(self):
        super().__init__()
        self.name = 'Random Agent'

    @staticmethod
    def get_action():
        return random.randint(0, 11)

    def update(self, result: LemonadeResult):
        pass
