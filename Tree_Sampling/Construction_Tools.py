import random
from TreeNode import TreeNode
import psutil
import os
from Visualization import visualize_tree

def random_tree_assigned(n):
    """Create a tree with n nodes assigned."""
    random_list = [random.randint(0, 10000000) for _ in range(n)]
    random_list.sort()
    return random_list

def construct_special_bst(sorted_array):
    if not sorted_array:
        return None

    if len(sorted_array) == 1:
        return TreeNode(val=sorted_array[0])

    # Find the middle point
    mid = len(sorted_array) // 2
    left_child = construct_special_bst(sorted_array[:mid])
    right_child = construct_special_bst(sorted_array[mid:])
    root_val = sorted_array[mid] # Update the root value
    root = TreeNode(val=root_val, left=left_child, right=right_child)
    return root

if __name__ == '__main__':
    random_list = random_tree_assigned(2500000)
    # 2500000 Nodes, memory cost is 1142.19MB
    root = construct_special_bst(random_list)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"当前程序的内存占用大小: {memory_info.rss / (1024 * 1024):.2f} MB")
    # visualize_tree(root,[])