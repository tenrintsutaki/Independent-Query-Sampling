import time

from Tree_Sampling import Construction_Tools
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    find_paths_and_collect, basic_sampling_preprocess
from Tree_Sampling.TreeNode import TreeNode

def calculate_time(root,selectivity,total_length):
    start = time.time()
    canonical, weights = find_paths_and_collect(root, random_list[0], random_list[int(total_length * selectivity)]) # Find the canonical nodes
    basic_sampling_preprocess(canonical, weights)
    for node in canonical: # Sample them to get the leaf.
        leaf_sampling(node)
    end = time.time()
    print(f"Time taken to sample {end - start} when selectivity is {selectivity}")
    return end - start

if __name__ == '__main__':
    # Test Methods of the Construction
    # 2500000 Nodes, memory cost is 1109.19MB
    num_nodes = 5000000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    root,leaf_index = construct_bst(random_list, weights, 0)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    for i in range(1,10):# ratio from 1% to 9%
        calculate_time(root,i / 10,num_nodes) # calculate the running time
    # Count the node amount in the interval
