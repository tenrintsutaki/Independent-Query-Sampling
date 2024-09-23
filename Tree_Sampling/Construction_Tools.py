import random
from TreeNode import TreeNode
import psutil
import os
import numpy as np
from Sample_Tools import find_min_in_right_subtree
from Visualization import visualize_tree

def random_tree_assigned(n):
    """Create a tree with n nodes assigned."""
    random_list = [random.randint(0, 2500000) for _ in range(n)]
    random_list.sort()
    return random_list

def construct_special_bst(sorted_array):
    if not sorted_array:
        return None

    if len(sorted_array) == 1: # For leaf nodes
        return TreeNode(val=sorted_array[0])

    mid = len(sorted_array) // 2
    left_child = construct_special_bst(sorted_array[:mid])
    right_child = construct_special_bst(sorted_array[mid:])
    root = TreeNode()
    root.val = find_min_in_right_subtree(right_child)
    root.left = left_child
    root.right = right_child
    return root

def generate_random_weights(num):
    random_weights = np.random.rand(num)
    total_weight = np.sum(random_weights)
    normalized_weights = random_weights / total_weight
    return normalized_weights

if __name__ == '__main__':
    # 2500000 Nodes, memory cost is 1109.19MB
    num_nodes = 2500000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    root = construct_special_bst(random_list)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"当前程序的内存占用大小: {memory_info.rss / (1024 * 1024):.2f} MB")
    # visualize_tree(root,[])