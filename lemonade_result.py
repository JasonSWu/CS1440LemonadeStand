class LemonadeResult:
    def __init__(self, actions, utils, index):
        self.reward = utils[index]
        self.opp_1_action = actions[(index + 1) % 3]
        self.opp_2_action = actions[(index + 2) % 3]
