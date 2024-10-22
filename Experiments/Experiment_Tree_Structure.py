import time
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes,calculate_height
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals
from Tree_Sampling.TreeNode import TreeNode
from Tree_Sampling.Sampling_Alias import leaf_sampling_alias, alias_sampling, alias_sampling_direct


def calculate_time_tree_sampling(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly
    for node in result:
        leaf_sampling(node) # Then use leaf sampling to get the result
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity}")
    return canonical

def calculate_time_tree_alias(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly using basic sample
    for node in result:
        leaf_sampling_alias(node) # Then use alias sampling to get the result
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Alias]")
    return end - start

def calculate_time_tree_alias_alias(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = alias_sampling(canonical, k) # Sample a canonical node firstly from AS Sampling*
    for node in result:
        leaf_sampling_alias(node) # Then use alias sampling to get the result
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Alias]")
    return end - start

def calculate_time_compare(root, selectivity, total_length,k):
    start = time.time()
    nodes = comparable_sampling(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    weights = [node.weight for node in nodes]  # 提取权重列表
    sampled_nodes = random.choices(nodes, weights=weights, k=k)
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Compare]")
    return end - start

def print_heights(node_list):
    res = []
    for node in node_list:
        res.append(calculate_height(node))
    return res

if __name__ == '__main__':
    # Test Methods of the Construction

    num_nodes = 1000000
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
    build_AS_structure(root)

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_cost_after_tree = memory_info.rss
    print(f"Memory Usage: {(memory_cost_after_tree - memory_cost_before_tree) / (1024 * 1024):.2f} MB")
    k  = 300
    round = 1
    root_height = calculate_height(root)
    for i in range(1, 100):  # ratio from 1% to 9%
        for r in range(round):
            canonicals = calculate_time_tree_sampling(root, i / 1000, num_nodes, k)  # calculate the running time
            print(f"height:  {max(print_heights(canonicals))}/{root_height}, selectivity = {i / 1000}")
