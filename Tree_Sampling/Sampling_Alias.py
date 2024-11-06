import random

from Alias.Alias_Structure import AliasStructure,AliasStructure_Direct_Nodes


def leaf_sampling_alias(node):
    if node.is_leaf():
        return node
    else:
        return node.AS.sample()

def leaf_sampling_alias_application(node):
    if node.is_leaf():
        return node
    else:
        return node.leaves[node.AS.sample()]
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

def alias_sampling_direct(canonical_nodes,times):
    probs = []
    results = []
    for node in canonical_nodes:
        probs.append(node.sample_weight)
    s = sum(probs)
    for i in range(len(probs)):
        probs[i] = probs[i] / s
    alias_structure = AliasStructure_Direct_Nodes(probs,canonical_nodes)
    alias_structure.initialize()
    for i in range(times):
        node = alias_structure.sample()
        results.append(node)
    return results