import time
import pandas as pd

from Chunk.builder import build_chunk, replace_non_align_chunk
from Construction_Tools import *
from Sample_Tools import calculate_weight, update_internal_nodes
from Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals

from Sampling_Alias import leaf_sampling_alias, alias_sampling, alias_sampling_direct
from Experiments.Exp_Generator import generate_random_interval
from Experiment_Space import calculate_tree_memory


def calculate_time_tree_sampling(root, selectivity, total_length,k):
    start = time.time()
    canonical, weights,l_align,r_align = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
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
    canonical, weights,l_align,r_align = find_paths_and_collect(root, random_list[start_index], random_list[end_index]) # Find the canonical nodes
    canonical = replace_non_align_chunk(canonical, l_align, r_align, random_list[start_index], random_list[end_index])
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
    canonical, weights,l_align,r_align = find_paths_and_collect(root, random_list[start_index], random_list[end_index]) # Find the canonical nodes
    canonical = replace_non_align_chunk(canonical, l_align, r_align, random_list[start_index], random_list[end_index])
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

    num_nodes = 250000
    chunk_size = 100
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    chunk_list = build_chunk(random_list, weights, chunk_size)
    root,leaf_index = construct_bst(chunk_list, weights) # 写一下
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root) #BUILD AS

    for k in [1000]:
        time_vals_canonical = []
        time_vals_compare = []
        time_vals_alias = []
        time_vals_alias_alias = []
        selectivity_vals = []
        round = 10
        extra_alias_memory = []
        for i in range(1,100):# ratio from 1% to 9%
            selectivity = random.random()
            r_canonical = []
            r_compare = 0
            r_alias = []
            r_alias_alias = []
            for r in range(round):
                # r_canonical.append(calculate_time_tree_sampling(root, selectivity, num_nodes,k)) # calculate the running time
                r_alias.append(calculate_time_tree_alias(root, selectivity, num_nodes, k))
                time_cost = calculate_time_tree_alias_alias(root, selectivity, num_nodes, k)
                r_alias_alias.append(time_cost)
            time_vals_canonical.append(r_canonical)
            time_vals_alias.append(r_alias)
            time_vals_alias_alias.append(r_alias_alias)
            selectivity_vals.append(selectivity)
        # Count the node amount in the interval

        x_values = []
        y_values = []
        y1_values = []
        y2_values = []

        # for i, yi in enumerate(time_vals_canonical):
        #     # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
        #     x_values.extend([selectivity_vals[i]] * len(yi))
        #     y_values.extend(yi)

        for i, yi in enumerate(time_vals_alias):
            # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
            x_values.extend([selectivity_vals[i]] * len(yi))
            y1_values.extend(yi)

        for i, yi in enumerate(time_vals_alias_alias):
            # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
            y2_values.extend(yi)

        data = {
            'Selectivity': x_values,
            # 'Tree_Traverse': y_values,
            'Alias': y1_values,
            'Double-Alias': y2_values
        }

        # 创建DataFrame
        df = pd.DataFrame(data)

        # 保存为CSV文件
        df.to_csv(f'data/N_{num_nodes}_s_{k}_chunk_{chunk_size}.csv', index=False)

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