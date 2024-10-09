import time
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals
from Tree_Sampling.TreeNode import TreeNode
from Tree_Sampling.Sampling_Alias import leaf_sampling_alias
def calculate_time_tree_sampling(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly
    for node in result:
        leaf_sampling(node) # Then use leaf sampling to get the result
    end = time.time()
    print(f"Time taken to sample {end - start} when selectivity is {selectivity}")
    return end - start

def calculate_time_tree_alias(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly
    for node in result:
        leaf_sampling_alias(node,k) # Then use alias sampling to get the result
    end = time.time()
    print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Alias]")
    return end - start

def calculate_time_compare(root, selectivity, total_length,k):
    start = time.time()
    nodes = comparable_sampling(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    weights = [node.weight for node in nodes]  # 提取权重列表
    sampled_nodes = random.choices(nodes, weights=weights, k=k)
    end = time.time()
    print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Compare]")
    return end - start

if __name__ == '__main__':
    # Test Methods of the Construction
    # 2500000 Nodes, memory cost is 1109.19MB
    num_nodes = 250000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)

    root,leaf_index = construct_bst(random_list, weights, 0)
    calculate_weight(root)
    update_internal_nodes(root)
    update_intervals(root)
    build_AS_structure(root)

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()

    time_vals_canonical = []
    time_vals_compare = []
    time_vals_alias = []
    selectivity_vals = []
    k = 100

    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    for i in range(1,10):# ratio from 1% to 9%
        time_canonical = calculate_time_tree_sampling(root, i / 10, num_nodes,k) # calculate the running time
        time_compare = calculate_time_compare(root, i / 10, num_nodes,k)
        time_alias = calculate_time_tree_alias(root, i / 10, num_nodes, k)
        time_vals_canonical.append(time_canonical)
        time_vals_compare.append(time_compare)
        time_vals_alias.append(time_alias)
        selectivity_vals.append(i / 10)
    # Count the node amount in the interval

    import numpy as np
    import matplotlib.pyplot as plt

    # Generate some sample data
    fig, ax1 = plt.subplots()
    # ax1.plot(selectivity_vals, time_vals_compare, label='Compare')
    ax1.plot(selectivity_vals, time_vals_alias, label='Alias')
    ax1.set_ylabel('Time')
    ax1.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    ax1.set_xlabel('Selectivity')
    ax1.legend()
    plt.title(f'Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    plt.show()
