from my_rl_lemonade_agent import LemonadeAgent, RandomAgent
from lemonade_result import LemonadeResult
from lemonade_helpers import get_utility
from sample_agent import StickAgent
import numpy as np


if __name__ == "__main__":
    agents = [LemonadeAgent(), LemonadeAgent(False), StickAgent(2)]
    total_u = np.zeros(3)
    for _ in range(10):
        actions = [agent.play_action() for agent in agents]
        utils = get_utility(actions)
        results = [LemonadeResult(actions, utils, i) for i in range(3)]
        for i, res in enumerate(results):
            agents[i].update_actions(res)
        total_u += utils
        # print(agents[2].my_actions[-1])
    s = ''
    for i in range(3):
        s += f'Agent {agents[i].name} got utility {total_u[i]} '
    print(s)
    print(agents[0].q_table)
    print(np.count_nonzero(agents[0].q_table - 12)) # agent is not learning
