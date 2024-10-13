import time
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals
from Tree_Sampling.TreeNode import TreeNode
from Tree_Sampling.Sampling_Alias import leaf_sampling_alias, alias_sampling


def calculate_time_tree_sampling(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly
    for node in result:
        leaf_sampling(node) # Then use leaf sampling to get the result
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity}")
    return end - start

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

if __name__ == '__main__':
    # Test Methods of the Construction
    num_nodes = 1200000
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
    time_vals_alias_alias = []
    selectivity_vals = []
    k = 200
    round = 10
    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    for i in range(1,10):# ratio from 1% to 9%
        r_canonical = 0
        r_compare = 0
        r_alias = 0
        r_alias_alias = 0
        for r in range(round):
            r_canonical += calculate_time_tree_sampling(root, i / 10, num_nodes,k) # calculate the running time
            r_compare += calculate_time_compare(root, i / 10, num_nodes,k)
            r_alias += calculate_time_tree_alias(root, i / 10, num_nodes, k)
            r_alias_alias += calculate_time_tree_alias_alias(root, i / 10, num_nodes, k)
        print(f"Time taken to sample {r_compare / round} when selectivity is {i / 10} [compare]")
        print(f"Time taken to sample {r_canonical / round} when selectivity is {i / 10} [canonical]")
        print(f"Time taken to sample {r_alias / round} when selectivity is {i / 10} [alias]")
        print(f"Time taken to sample {r_alias_alias / round} when selectivity is {i / 10} [alias-alias]")
        time_vals_canonical.append(r_canonical / round)
        time_vals_compare.append(r_compare / round)
        time_vals_alias.append(r_alias / round)
        time_vals_alias_alias.append(r_alias_alias / round)
        selectivity_vals.append(i / 10)
    # Count the node amount in the interval

    import numpy as np
    import matplotlib.pyplot as plt

    # Generate some sample data
    fig1, ax1 = plt.subplots()
    ax1.plot(selectivity_vals, time_vals_compare, label='Compare')
    ax1.plot(selectivity_vals, time_vals_alias, label='Alias')
    ax1.set_ylabel('Time')
    ax1.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    ax1.set_xlabel('Selectivity')
    ax1.legend()
    plt.title(f'Nodes: {num_nodes}, Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    plt.show()

    fig2, ax2 = plt.subplots()
    ax2.plot(selectivity_vals, time_vals_alias, label='Alias')
    ax2.plot(selectivity_vals, time_vals_alias_alias, label='Alias-Alias')
    ax2.set_ylabel('Time')
    ax2.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    ax2.set_xlabel('Selectivity')
    ax2.legend()
    plt.title(f'Nodes: {num_nodes}, Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    plt.show()
