import random


def leaf_sampling_alias(node,k):
    if node.is_leaf():
        return node
    for i in range(k): # Low efficient, need to be modified
        return node.AS.sample()
