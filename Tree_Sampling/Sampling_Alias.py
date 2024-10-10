import random

from Alias.Alias_Structure import AliasStructure


def leaf_sampling_alias(node):
    if node.is_leaf():
        return node
    else:
        return node.AS.sample()
def alias_sampling(canonical_nodes,times):
    probs = []
    results = []
    for node in canonical_nodes:
        probs.append(node.sample_weight)
    s = sum(probs)
    for i in range(len(probs)):
        probs[i] = probs[i] / s
    alias_structure = AliasStructure(probs)
    alias_structure.initialize()
    for i in range(times):
        result_index = alias_structure.sample()
        results.append(canonical_nodes[result_index])
    return results