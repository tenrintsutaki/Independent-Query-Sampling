import random

from Tree_Sampling.Sampling import find_paths_and_collect, basic_sampling, basic_sampling_preprocess
import random

from Tree_Sampling.Sampling_Alias import alias_sampling, leaf_sampling_alias


def calculate_records_num(canonical_nodes):
    s = 0
    for node in canonical_nodes:
        s += node.weight
    return s

def sampling_application(root,left_val,right_val,k,df):
    canonical, weights = find_paths_and_collect(root,left_val,right_val) # Find the canonical nodes
    total_records_num = calculate_records_num(canonical)
    basic_sampling_preprocess(canonical, weights)
    result = alias_sampling(canonical, k) # Sample a canonical node firstly from AS Sampling*
    temp = []
    for node in result:
        res = leaf_sampling_alias(node) # Then use alias sampling to get the result
        temp.append(res)
    return temp,total_records_num

