import random

from Alias.Alias_Structure import AliasStructure,AliasStructure_Direct_Nodes
from Tree_Sampling.TreeNode import TreeNode
import psutil
import os
import numpy as np
from Tree_Sampling.Sample_Tools import find_min_in_right_subtree,find_leaves

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
    ls = random.sample(range(100 * n), n)
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

def construct_bst_with_element(sorted_array, weights, elements, leaf_index = 0):
    if not sorted_array:
        return None, leaf_index

    if len(sorted_array) == 1: # For leaf nodes
        weight = weights[leaf_index]
        leaf_index = leaf_index + 1
        ptrs = elements[sorted_array[0]]
        return TreeNode(val = sorted_array[0], weight = weight, ptrs = ptrs), leaf_index

    mid = len(sorted_array) // 2
    left_child,leaf_index  = construct_bst_with_element(sorted_array[:mid], weights, elements, leaf_index)
    right_child,leaf_index = construct_bst_with_element(sorted_array[mid:], weights, elements, leaf_index)
    root = TreeNode()
    root.val = find_min_in_right_subtree(right_child)
    root.left = left_child
    root.right = right_child
    return root,leaf_index

def build_AS_structure(root):
    """
    Build the AS structure for the BST
    :param root:
    :return:
    """
    if not root:
        return

    if root.is_leaf():
        return

    leaves = find_leaves(root) # find leaves belonging to this node
    probs = []
    for leaf in leaves:
        probs.append(leaf.weight) # Not sure for sample weight or weight
    s = sum(probs)
    for i in range(0,len(probs)): # Can be low efficient, need to be modified
        probs[i] /= s
    alias_structure = AliasStructure(probs)
    alias_structure.elements = leaves # Add leaves to elements 存叶子
    root.AS = alias_structure
    root.AS.initialize()
    # root.leaves = leaves
    build_AS_structure(root.left)
    build_AS_structure(root.right)

def build_AS_structure_direct_node(root):
    """
    Build the AS structure for the BST
    :param root:
    :return:
    """
    if not root:
        return

    if root.is_leaf():
        return

    leaves = find_leaves(root) # find leaves belonging to this node
    probs = []
    for leaf in leaves:
        probs.append(leaf.weight) # Not sure for sample weight or weight
    s = sum(probs)
    for i in range(0,len(probs)): # Can be low efficient, need to be modified
        probs[i] /= s
    alias_structure = AliasStructure_Direct_Nodes(probs,leaves)
    root.AS = alias_structure
    root.AS.initialize()

    build_AS_structure(root.left)
    build_AS_structure(root.right)

def generate_random_weights(num):
    random_weights = np.random.rand(num)
    total_weight = np.sum(random_weights)
    normalized_weights = random_weights / total_weight
    return normalized_weights

def generate_normal_like_weights(lo,hi,num):
    random_weights = np.random.uniform(lo,hi,num)
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
    num_nodes = 25000
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    root,leaf_index = construct_bst(random_list, weights, 0)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    # visualize_tree(root,[])