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
    start_index,end_index = generate_random_interval(selectivity, total_length)
    canonical, weights = find_paths_and_collect(root,random_list[start_index],random_list[end_index]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sample a canonical node firstly using basic sample
    for node in result:
        leaf_sampling_alias(node) # Then use alias sampling to get the result
    end = time.time()
    # print(f"Time taken to sample {end - start} when selectivity is {selectivity} [Alias]")
    return end - start

def calculate_time_tree_alias_alias(root, selectivity, total_length,k):
    start = time.time()
    start_index,end_index = generate_random_interval(selectivity, total_length)
    canonical, weights = find_paths_and_collect(root,start_index,end_index) # Find the canonical nodes
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
    build_AS_structure(root) #BUILD AS

    print(f"Memory Cost of Tree: {calculate_tree_memory(root) / (1024 * 1024 * 1024)} GB")

    time_vals_canonical = []
    time_vals_compare = []
    time_vals_alias = []
    time_vals_alias_alias = []
    selectivity_vals = []
    s = 1
    k = int((s / 1000) * num_nodes)
    round = 10
    for i in range(1,100):# ratio from 1% to 9%
        selectivity = random.random()
        r_canonical = []
        r_compare = 0
        r_alias = []
        r_alias_alias = []
        for r in range(round):
            r_canonical.append(calculate_time_tree_sampling(root, selectivity, num_nodes,k)) # calculate the running time
            # r_compare += calculate_time_compare(root, i / 10, num_nodes,k)
            r_alias.append(calculate_time_tree_alias(root, selectivity, num_nodes, k))
            r_alias_alias.append(calculate_time_tree_alias_alias(root, selectivity, num_nodes, k))
        # print(f"Time taken to sample {r_compare / round} when selectivity is {i / 10} [compare]")
        # print(f"Time taken to sample {r_canonical / round} when selectivity is {i / 10} [canonical]")
        # print(f"Time taken to sample {r_alias / round} when selectivity is {i / 10} [alias]")
        # print(f"Time taken to sample {r_alias_alias / round} when selectivity is {i / 10} [alias-alias]")
        time_vals_canonical.append(r_canonical)
        # time_vals_compare.append(r_compare / round)
        time_vals_alias.append(r_alias)
        time_vals_alias_alias.append(r_alias_alias)
        selectivity_vals.append(selectivity)
    # Count the node amount in the interval

    import numpy as np
    import matplotlib.pyplot as plt

    # Generate some sample data
    # fig1, ax1 = plt.subplots()
    # ax1.plot(selectivity_vals, time_vals_compare, label='Compare')
    # ax1.plot(selectivity_vals, time_vals_alias, label='Alias')
    # ax1.set_ylabel('Time')
    # ax1.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    # ax1.set_xlabel('Selectivity')
    # ax1.legend()
    # plt.title(f'Nodes: {num_nodes}, Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    # plt.show()
    # 展开 y 列表，同时复制相应的 x 值

    x_values = []
    y_values = []
    y1_values = []
    y2_values = []

    for i, yi in enumerate(time_vals_canonical):
        # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
        x_values.extend([selectivity_vals[i]] * len(yi))
        y_values.extend(yi)

    for i, yi in enumerate(time_vals_alias):
        # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
        y1_values.extend(yi)

    for i, yi in enumerate(time_vals_alias_alias):
        # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
        y2_values.extend(yi)

    data = {
        'Selectivity': x_values,
        'Tree_Traverse': y_values,
        'Alias': y1_values,
        'Double-Alias': y2_values
    }

    # 创建DataFrame
    df = pd.DataFrame(data)

    # # 保存为CSV文件
    # df.to_csv(f'data/N_{num_nodes}_s_{s}.csv', index=False)

    #
    # plt.figure(figsize=(5, 8))
    # plt.scatter(x_values, y_values, label='Alias')
    # plt.scatter(x_values, y2_values, label='Alias-Alias')
    # plt.ylabel('Time')
    # # ax2.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    # plt.xlabel('Selectivity')
    # plt.legend()
    # plt.title(f'Nodes: {num_nodes}, Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    # plt.show()
    # # 图拉得高一些，坐标轴需要变换一下