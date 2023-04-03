import numpy as np


def get_utility(actions):
    l1 = actions[0]
    l2 = actions[1]
    l3 = actions[2]
    assert l1 <= 11, "Location must be 0-11"
    assert l2 <= 11, "Location must be 0-11"
    assert l3 <= 11, "Location must be 0-11"
    if l1 == l2 and l2 == l3:
        utils = [8, 8, 8]
    elif l1 == l2:
        utils = [6, 6, 12]
    elif l2 == l3:
        utils = [12, 6, 6]
    elif l1 == l3:
        utils = [6, 12, 6]
    else:
        new_values, new_indices = sort_and_get_indices([l1, l2, l3])
        u1 = new_values[1] - new_values[0]
        u2 = new_values[2] - new_values[1]
        u3 = 12 + new_values[0] - new_values[2]
        utils = [0]*3
        utils[new_indices[0]] = u1 + u3
        utils[new_indices[1]] = u1 + u2
        utils[new_indices[2]] = u2 + u3
    return np.array(utils)


def sort_and_get_indices(values):
    sorted_values = sorted(values)
    index_map = {value: index for index, value in enumerate(values)}
    sorted_indices = [index_map[value] for value in sorted_values]

    return sorted_values, sorted_indices
