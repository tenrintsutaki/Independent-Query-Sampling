import time

from Tree_Sampling import Construction_Tools
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling
from Tree_Sampling.TreeNode import TreeNode

def calculate_time(canonical,sq_size,ratio):
    start = time.time()
    sampled_nodes = basic_sampling(canonical, int(sq_size * ratio)) # Get 1st sampled nodes (from canonical)
    for node in sampled_nodes: # Sample them to get the leaf.
        leaf_sampling(node)
    end = time.time()
    print(f"Time taken to sample {end - start} seconds when sq_size is {sq_size}, ratio is {ratio}")
    return end - start

if __name__ == '__main__':
    # Test Methods of the Construction
    # 2500000 Nodes, memory cost is 1109.19MB
    num_nodes = 2500000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    root,leaf_index = construct_bst(random_list, weights, 0)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    canonical, weights = find_canonical_nodes_new(root, random_list[5], random_list[15]) # Find the canonical nodes
    num_leaves = calculate_leaf_numbers(canonical)
    print(f"Number of leaves: {num_leaves}")
    for i in range(1,9):# ratio from 0.1 to 0.9
        calculate_time(canonical,num_leaves,i / 10) # calculate the running time
    # Count the node amount in the interval
