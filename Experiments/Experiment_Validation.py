import time
import pandas as pd
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

def calculate_time_tree_alias_alias(root, selectivity, total_length,k,t):
    start = time.time()
    start_index,end_index = generate_random_interval(selectivity, total_length)
    canonical, weights = find_paths_and_collect(root,start_index,end_index) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result,memory_overhead = alias_sampling(canonical, k) # Sample a canonical node firstly from AS Sampling*
    for node in result:
        leaf = leaf_sampling_alias(node) # Then use alias sampling to get the result
        t.add_record(leaf.val)
    end = time.time()
    return end - start, memory_overhead

if __name__ == '__main__':
    # Test Methods of the Construction

    num_nodes = 10000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_cost_before_tree = memory_info.rss

    root,leaf_index = construct_bst(random_list, weights, 0)
    calculate_weight(root)
    update_internal_nodes(root)
    # update_intervals(root)
    # build_AS_structure_direct_node(root)
    build_AS_structure(root) #BUILD AS
    t = Tester(random_list, weights,0.1)

    for k in [10000]:
        time_vals_alias_alias = []
        selectivity_vals = []
        round = 1
        extra_alias_memory = []
        for i in range(1,2):# ratio from 1% to 9%
            selectivity = random.random()
            r_alias_alias = []
            for r in range(round):
                time_cost,memory = calculate_time_tree_alias_alias(root, selectivity, num_nodes, k, t)
    t.valid()
