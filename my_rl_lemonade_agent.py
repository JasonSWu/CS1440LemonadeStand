from agent import Agent
from lemonade_result import LemonadeResult
from lemonade_helpers import get_utility
import random
import numpy as np
from sample_agent import StickAgent

def getmindist(x, y):
    return min((x-y) % 12, (y-x) % 12)

class LemonadeAgent(Agent):
    def __init__(self, train=True):
        # TODO: Name agent and implement any additional class characteristics you may need
        super().__init__()
        self.name = 'UConnDub'
        self.num_states = 1296
        self.q_table = np.array([[12 for _ in range(12)] for _ in range(self.num_states)], dtype=float)
        self.discount_rate = 0.95
        self.dev_tolerance = 2
        self.state = 0
        self.threshold = 0
        self.learning_rate = 0.5
        self.opponent_states = [0, 0]
        self.counter = 0
        if train:
            self.train()

    def get_action(self):
        # TODO: Enter logic to pick next result here
        # this method is ran before update()
        state = self.state # changed
        action = np.random.choice(np.flatnonzero(self.q_table[self.state] == self.q_table[self.state].max()))
        self.counter += 1
        # print(f"action counter: {self.counter}")
        return action # returns an int 0-11

    def update(self, result: LemonadeResult):
        # TODO: Enter any logic you'd like to include in the update. Please check the base class update_actions before
        # part (a)
        # calculate f_i0, f_ij, l_i for all players and threshold B
        if self.counter > 102:
            del self.my_actions[0]
            del self.my_rewards[0]
            del self.opponent_1_actions[0]
            del self.opponent_2_actions[0]
            self.counter -= 1
        l_1 = 0
        l_2 = 0
        f_10 = 0
        f_12 = 0
        f_20 = 0
        f_21 = 0
        if self.counter >= 3:
            self.threshold = 0
            Gamma = 0
            for k in range(2, self.counter):
                Gamma += self.discount_rate**(self.counter - 1 - k)
            for k in range(2, self.counter):
                self.threshold -= (self.discount_rate**(self.counter-1-k)/Gamma)
                l_1 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_1_actions[k], self.opponent_1_actions[k-1])**self.dev_tolerance
                l_2 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_2_actions[k], self.opponent_2_actions[k-1])**self.dev_tolerance
                f_10 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_1_actions[k], ((self.my_actions[k-1] + 6) % 12))**self.dev_tolerance
                f_12 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_1_actions[k], ((self.opponent_2_actions[k-1] + 6) % 12))**self.dev_tolerance
                f_20 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_2_actions[k], ((self.my_actions[k-1] + 6) % 12))**self.dev_tolerance
                f_21 -= ((self.discount_rate**(self.counter-1-k))/Gamma) * getmindist(self.opponent_2_actions[k], ((self.opponent_1_actions[k-1] + 6) % 12))**self.dev_tolerance
            self.threshold *= 6**(self.dev_tolerance)
            self.threshold *= 0.4
        else:
            l_1 = -1
            l_2 = -1
            f_10 = -1
            f_12 = -1
            f_20 = -1
            f_21 = -1
        
        # print(f"threshold: {self.threshold}")
        # print("opponent 1")
        # print(f"f_10: {f_10}")
        # print(f"f_12: {f_12}")
        # print(f"l_1: {l_1}")
        # print("opponent 2")
        # print(f"f_20: {f_20}")
        # print(f"f_21: {f_21}")
        # print(f"l_2: {l_2}")
        if f_10 >= self.threshold:
            self.opponent_states[0] = 0
        elif f_12 >= self.threshold:
            self.opponent_states[0] = 1
        elif l_1 >= self.threshold:
            self.opponent_states[0] = 2
        else:
            self.opponent_states[0] = 3

        if f_20 >= self.threshold:
            self.opponent_states[1] = 0
        elif f_21 >= self.threshold:
            self.opponent_states[1] = 1
        elif l_2 >= self.threshold:
            self.opponent_states[1] = 2
        else:
            self.opponent_states[1] = 3

        # update state
        old_state = self.state
        l = len(self.opponent_1_actions)
        temp1 = 0
        for i in range(2):
            temp1 *= 4
            temp1 += self.opponent_states[i]
        temp2 = 0
        for i in range(1, 3):
            if (i > l):
                break
            temp2 *= 3
            temp2 += (self.opponent_1_actions[-i] // 4)
        temp3 = 0
        for i in range(1, 3):
            if (i > l):
                break
            temp3 *= 3
            temp3 += (self.opponent_2_actions[-i] // 4)
        self.state = (temp1*9 + temp2)*9 + temp3

        print(f"curr state: {self.state}, old state: {old_state}") # we are going to different states
        print(f"old value: {self.q_table[old_state, self.my_actions[-1]]}")
        print(f"reward: {self.my_rewards[-1]}")
        # why is this ballooning?
        self.q_table[old_state, self.my_actions[-1]] = self.learning_rate*(self.my_rewards[-1] + self.discount_rate*np.max(self.q_table[self.state])) + (1 - self.learning_rate)*self.q_table[old_state, self.my_actions[-1]]
        print(f"max value: {np.max(self.q_table[self.state])}")
        print(f"new value: {self.q_table[old_state, self.my_actions[-1]]}")
        
                                                                             
    def train(self):
        # play against two versions of itself
        # play 100,000 rounds then reset relavent variables
        print("training")
        adversary1 = RandomAgent()
        print("no train")
        adversary2 = StickAgent(4)
        print("no train")
        self.threshold = 0
        agents = [self, adversary1, adversary2]

        for loop in range(10000): # change back
            print(loop)
            my_action = np.random.choice(range(12))
            self.my_actions.append(my_action)
            actions = [my_action, adversary1.play_action(), adversary2.play_action()]
            utils = get_utility(actions)
            results = [LemonadeResult(actions, utils, i) for i in range(3)]
            for i, res in enumerate(results):
                agents[i].update_actions(res)
        print(np.count_nonzero(self.q_table - 12))
        print("done")
        print(self.q_table)
        self.cleanup()
    
    def cleanup(self):
        # qtable = self.q_table
        self.my_actions = []
        self.my_rewards = []
        self.opponent_1_actions = []
        self.opponent_2_actions = []
        # self.name = 'UConnDub'
        # self.num_states = 1296
        # self.discount_rate = 0.9
        # self.dev_tolerance = 2
        # self.state = 0
        # self.threshold = 0
        # self.learning_rate = 0.5
        self.opponent_states = [0, 0]
        self.counter = 0
        

class RandomAgent(LemonadeAgent):
    def __init__(self, train=False):
        super().__init__(False)
        self.name = 'Random Agent'

    @staticmethod
    def get_action():
        return random.randint(0, 11)

    def update(self, result: LemonadeResult):
        pass
