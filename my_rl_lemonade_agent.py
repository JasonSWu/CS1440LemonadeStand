from agent import Agent
from lemonade_result import LemonadeResult
import random
import numpy as np


class LemonadeAgent(Agent):
    def __init__(self, num_states, starting_val, discount_rate, scale, epsilon, dev_tolerance, kappa):
        # TODO: Name agent and implement any additional class characteristics you may need
        super().__init__()
        self.name = '------'
        # 12 is possible actions
        # what is s?
        # altered self.q_table
        # (12, 12) is (initial_state_score, num_possible_actions)
        self.q_table = np.array([[12 for _ in range(12)] for _ in range(num_states)])
        # self.q_table = {s: [starting_val for _ in range(12)] for _ in range(num_states)} # edited
        # self.move = random.randint(0, 11) # first move
        self.discount_rate = discount_rate
        self.scale = scale
        self.epsilon = epsilon 
        # epsilon can be chosen arbitrarily small to be optimistic in the face of uncertainty.
        self.dev_tolerance = dev_tolerance
        self.kappa = kappa # currently arbitrary
        self.state = 0
        self.threshold = 0
        self.count = np.zeros((num_states, 12))
        self.learning_rate = 0.5
        self.opponent_states = [0, 0]

    def get_action(self):
        # TODO: Enter logic to pick next result here
        # this method is ran before update()
        state = self.state # changed
        action = np.argmax(self.q_table[state])
        return action # returns an int 0-11

    def update(self, result: LemonadeResult):
        # TODO: Enter any logic you'd like to include in the update. Please check the base class update_actions before
        # part (a)
        # update state first
        old_state = self.state
        l = len(self.opponent_1_actions)
        temp1 = 0
        for i in range(2):
            # based on f_ij
            temp1 *= 4
            temp1 += self.opponent_states[i]
        temp2 = 0
        for i in range(1, 3):
            if (i > l):
                break
            temp2 *= 3
            temp2 += (self.opponent_1_actions[-i] // 4)
        self.state += temp
        temp = 0
        for i in range(1, 3):
            if (i > l):
                break
            
        # calculate f_i0, f_ij, l_i for all players and threshold B
        self.q_table[self.state, self.my_actions[-1]] = self.learning_rate*(self.my_rewards[-1] + np.max(self.q_table[]))
        # what if we incorporate opponent states into num_states?
        # their states and last two actions (4*4*3^4*12) - q_table size

        # part (b)
        # update state
        def update_state():

            pass
        # updating count
        self.count[self.state, self.my_actions[-1]] += 1
        # updating utility u(s,a) += r(a)
        self.q[self.state] += 
        #  changing this
        
        pass


    def train(self):
        # play against two versions of itself
        # play 100,000 rounds then reset relavent variables
        self.count = np.zeros((self.num_states, 12))
        self.threshold = 0
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
