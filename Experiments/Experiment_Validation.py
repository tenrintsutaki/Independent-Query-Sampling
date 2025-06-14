import time
import pandas as pd
from matplotlib import pyplot as plt

from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals
from Tree_Sampling.TreeNode import TreeNode
from Tree_Sampling.Sampling_Alias import leaf_sampling_alias, alias_sampling, alias_sampling_direct
from Experiments.Exp_Generator import generate_random_interval
from Experiment_Space import calculate_tree_memory
from pympler import asizeof
from Validation.Result_Tester import Tester
from Tree_Sampling.Construction_Tools import calculate_leaf_numbers
def calculate_time_tree_alias_alias(root, random_list, selectivity, total_length,k,t):
    start = time.time()
    start_index,end_index = generate_random_interval(selectivity, total_length)
    canonical, weights = find_paths_and_collect(root,random_list[start_index],random_list[end_index])
    basic_sampling_preprocess(canonical, weights)
    result,memory_overhead = alias_sampling(canonical, k) # Sample a canonical node firstly from AS Sampling*
    for node in result:
        leaf = leaf_sampling_alias(node) # Then use alias sampling to get the result
        t.add_record(leaf.val)
    end = time.time()
    return end - start, memory_overhead

if __name__ == '__main__':
    # Test Methods of the Construction

    num_nodes = 50000
    lo = 3
    hi = 7
    random_list = random_tree_assigned(num_nodes)
    weights = generate_normal_like_weights(lo,hi,num_nodes)
    root,leaf_index = construct_bst(random_list, weights, 0)
    calculate_weight(root)
    update_internal_nodes(root)
    # update_intervals(root)
    # build_AS_structure_direct_node(root)
    build_AS_structure(root) #BUILD AS

    for k in [2500000]:
        t = Tester(random_list, weights, 0.1)
        # for k in [10000, 50000, 100000, 500000]:
        selectivity = 0.6
        time_cost,memory = calculate_time_tree_alias_alias(root, random_list, selectivity, num_nodes, k, t)
        result_factors = t.valid()
        plt.figure(figsize=(10, 6))
        plt.axhline(y=1, color='red', linestyle='-')
        plt.ylim(0,2)
        plt.scatter([i for i in range(len(result_factors))],result_factors)
        plt.title(f"Validation N = {num_nodes} with s = {k}")
        plt.ylabel("f (Factor)")
        plt.xlabel("element")
        print(len(result_factors))
        # plt.title(f"Validation with s = {k}, p = {p_value}")
        # plt.show()
        plt.savefig(f"data/validation_figs/N_{num_nodes}_s_{k}_valid.png", dpi=300, bbox_inches="tight")  # 保存为 PNG 文件

