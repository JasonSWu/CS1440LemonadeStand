from my_lemonade_agent import LemonadeAgent, RandomAgent
from lemonade_result import LemonadeResult
from lemonade_helpers import get_utility
from sample_agent import StickAgent
import numpy as np


if __name__ == "__main__":
    agents = [LemonadeAgent(), LemonadeAgent(), StickAgent(2)]
    total_u = np.zeros(3)
    for _ in range(10):
        actions = [agent.play_action() for agent in agents]
        utils = get_utility(actions)
        results = [LemonadeResult(actions, utils, i) for i in range(3)]
        for i, res in enumerate(results):
            agents[i].update_actions(res)
        total_u += utils
    s = ''
    for i in range(3):
        s += f'Agent {agents[i].name} got utility {total_u[i]} '
    print(s)
