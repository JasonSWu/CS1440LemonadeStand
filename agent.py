import abc
from lemonade_result import LemonadeResult


class Agent(metaclass=abc.ABCMeta):
    def __init__(self):
        self.my_actions = []
        self.my_rewards = []
        self.opponent_1_actions = []
        self.opponent_2_actions = []

    @abc.abstractmethod
    def get_action(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, result: LemonadeResult):
        raise NotImplementedError

    def update_actions(self, result: LemonadeResult):
        self.opponent_1_actions.append(result.opp_1_action)
        self.opponent_2_actions.append(result.opp_2_action)
        self.my_rewards.append(result.reward)
        self.update(result)

    def play_action(self):
        action = self.get_action()
        self.my_actions.append(action)
        return action

    def new_game(self):
        self.__init__()