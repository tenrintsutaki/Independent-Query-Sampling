import random
from Tree_Sampling.TreeNode import TreeNode
import psutil
import os
import numpy as np
from Tree_Sampling.Sample_Tools import find_min_in_right_subtree
#TODO: Finish the boundary case problem.
#TODO: Try to do the sampling method.

def random_tree_assigned(n):
    """
        Create a tree with n nodes assigned.
        Only includes the unique nodes.
    """
    # random_list = []
    # for _ in range(n):
    #     r = random.randint(0, 2500000)
    #     if r not in random_list:
    #         random_list.append(r)
    # random_list.sort()
    ls = random.sample(range(10 * n), n)
    ls.sort()
    return ls

def construct_bst(sorted_array, weights, leaf_index = 0):
    if not sorted_array:
        return None, leaf_index

    if len(sorted_array) == 1: # For leaf nodes
        weight = weights[leaf_index]
        leaf_index = leaf_index + 1
        return TreeNode(val = sorted_array[0], weight = weight), leaf_index

    mid = len(sorted_array) // 2
    left_child,leaf_index  = construct_bst(sorted_array[:mid], weights, leaf_index)
    right_child,leaf_index = construct_bst(sorted_array[mid:], weights, leaf_index)
    root = TreeNode()
    root.val = find_min_in_right_subtree(right_child)
    root.left = left_child
    root.right = right_child
    return root,leaf_index

def generate_random_weights(num):
    random_weights = np.random.rand(num)
    total_weight = np.sum(random_weights)
    normalized_weights = random_weights / total_weight
    return normalized_weights

def calculate_leaf_numbers(nodes):
    """ find how many leaf nodes in these input {nodes} """
    res = 0
    def count_leaf_nodes(root):
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return 1
        return count_leaf_nodes(root.left) + count_leaf_nodes(root.right)

    for node in nodes:
        count = count_leaf_nodes(node)
        print(f"count: {count}")
        res += count
    return res

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
    # visualize_tree(root,[])