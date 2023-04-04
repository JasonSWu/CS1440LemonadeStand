from my_rl_lemonade_agent_2 import LemonadeAgent, RandomAgent
from lemonade_result import LemonadeResult
from lemonade_helpers import get_utility
from sample_agent import StickAgent
import numpy as np


if __name__ == "__main__":
    agents = [LemonadeAgent(), LemonadeAgent(), RandomAgent()]
    total_u = np.zeros(3)
    NUM_ROUNDS = 100
    for _ in range(NUM_ROUNDS):
        actions = [agent.play_action() for agent in agents]
        utils = get_utility(actions)
        results = [LemonadeResult(actions, utils, i) for i in range(3)]
        for i, res in enumerate(results):
            agents[i].update_actions(res)
        total_u += utils
    s = ''
    for i in range(3):
        s += f'Agent {agents[i].name} got utility {total_u[i] / NUM_ROUNDS} '
    print(s)
    print(agents[0].q_table)
    print(f"number of non-zero q-table values: {np.count_nonzero(agents[0].q_table)} out of 1944") # agent is not learning properly in paper implementation
