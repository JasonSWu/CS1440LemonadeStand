from agent import Agent
from lemonade_result import LemonadeResult
from lemonade_helpers import get_utility
import random
import numpy as np
from sample_agent import StickAgent

def getminl2dist(x, y):
    return min(((x-y) % 12)**2, ((y-x) % 12)**2)

class LemonadeAgent(Agent):
    def __init__(self, train=True):
        # TODO: Name agent and implement any additional class characteristics you may need
        super().__init__()
        self.name = 'UConnDub'
        self.num_states = 4*81 # try 4 vs 9
        self.q_table = np.array([[0 for _ in range(6)] for _ in range(self.num_states)], dtype=float)
        self.discount_rate = 0.9
        self.state = 0
        self.learning_rate = 0.05
        self.exploration_rate = 0.15
        if train:
            self.train()

    def get_action(self):
        action = np.random.choice(np.flatnonzero(self.q_table[self.state] == self.q_table[self.state].max()))
        action = (random.randint(2*action, 2*action + 1) + 1) % 12
        return action 

    def update(self, result: LemonadeResult):
        l = len(self.opponent_1_actions)

        temp1 = 0
        # add discount factor
        if l < 4:
            dist_1 = np.sum([getminl2dist(x,y)*self.discount_rate**(len(self.my_actions) - 1 - i) for i,(x,y) in enumerate(zip(self.my_actions, self.opponent_1_actions))])
            dist_2 = np.sum([getminl2dist(x,y)*self.discount_rate**(len(self.my_actions) - 1 - i) for i,(x,y) in enumerate(zip(self.my_actions, self.opponent_2_actions))])
        else:
            dist_1 = np.sum([getminl2dist(x,y)*self.discount_rate**(3 - i) for i,(x,y) in enumerate(zip(self.my_actions[-4:], self.opponent_1_actions[-4:]))])
            dist_2 = np.sum([getminl2dist(x,y)*self.discount_rate**(3 - i) for i,(x,y) in enumerate(zip(self.my_actions[-4:], self.opponent_2_actions[-4:]))])
        if dist_1 >= 55:
            temp1 += 1
        # elif dist_1 >= 11:
        #     temp1 += 1
        temp1 *= 2
        if dist_2 >= 55:
            temp1 += 1
        # elif dist_2 >= 11:
        #     temp1 += 1

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

        # update state
        old_state = self.state
        action = np.argmax(self.q_table[old_state])
        self.q_table[old_state, action] = self.learning_rate*(self.my_rewards[-1] - 7.5 + self.discount_rate*np.max(self.q_table[self.state])) + (1 - self.learning_rate)*self.q_table[old_state, action]
        # TRY 7.5 vs 8
                                                                             
    def train(self):
        # play against two versions of itself
        # play 100,000 rounds then reset relavent variables
        adversary1 = LemonadeAgent(False)
        adversary2 = LemonadeAgent(False)
        agents = [self, adversary1, adversary2]
        for loop in range(100000): 
            print(loop)
            my_action = self.choose_next_move()
            self.my_actions.append(my_action)
            actions = [my_action, adversary1.play_action(), adversary2.play_action()]
            utils = get_utility(actions)
            results = [LemonadeResult(actions, utils, i) for i in range(3)]
            for i, res in enumerate(results):
                agents[i].update_actions(res)
        self.cleanup()

        # adversary1 = RandomAgent(False)
        # adversary2 = LemonadeAgent(False)

        # for loop in range(50000): 
        #     print(50000 + loop)
        #     my_action = self.choose_next_move()
        #     self.my_actions.append(my_action)
        #     actions = [my_action, adversary1.play_action(), adversary2.play_action()]
        #     utils = get_utility(actions)
        #     results = [LemonadeResult(actions, utils, i) for i in range(3)]
        #     for i, res in enumerate(results):
        #         agents[i].update_actions(res)
        # self.cleanup()
    
    def choose_next_move(self):
        if np.random.uniform() <= self.exploration_rate:
            # find zero tables choices
            zero_indices = np.flatnonzero(self.q_table[self.state] == 0) # works properly
            if zero_indices.size != 0:
                return np.random.choice(zero_indices)
            else:
                return np.random.choice(range(12))
        else:
            return self.get_action()
    
    def cleanup(self):
        self.my_actions = []
        self.my_rewards = []
        self.opponent_1_actions = []
        self.opponent_2_actions = []
                

class RandomAgent(LemonadeAgent):
    def __init__(self, train=False):
        super().__init__(False)
        self.name = 'Random Agent'

    @staticmethod
    def get_action():
        return random.randint(0, 11)

    def update(self, result: LemonadeResult):
        pass
