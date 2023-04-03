from agent import Agent
from lemonade_result import LemonadeResult
import random
import numpy as np


class LemonadeAgent(Agent):
    def __init__(self, num_states, starting_val):
        # TODO: Name agent and implement any additional class characteristics you may need
        super().__init__()
        self.name = 'EnterNameHere'
        self.q_table = {s: [starting_val for _ in range(12)] for _ num_states}

    def get_action(self):
        # TODO: Enter logic to pick next result here
        state = None
        action = np.argmax(self.q_table[state])
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
