# 绘制二叉树的递归函数
from collections import defaultdict

from matplotlib import pyplot as plt

from Experiments.Experiment_Space import calculate_tree_memory
from pympler import asizeof
from TreeNode import TreeNode
from Sampling import *
from Sample_Tools import update_internal_nodes,traverse_path,calculate_weight,find_leaves,calculate_height
from Tree_Sampling.Construction_Tools import calculate_leaf_numbers
from Validation.Result_Tester import Tester


def plot_tree(node, canonical, x=0, y=0, layer=1, dx=1):
    if node is not None:
        # 在当前节点位置绘制节点值
        if node in canonical:
            color = "red"
        else:
            color = "skyblue"

        if not node.is_leaf():
            plt.text(x, y, str(node.val), ha='center', va='center', fontsize=12,
                     bbox=dict(facecolor=color, edgecolor='black', boxstyle='circle,pad=0.5'))
            plt.text(x + 0.3, y, "w=" + str(node.weight), ha='center', va='center', fontsize=12)
        else:
            plt.text(x, y, str(node.val), ha='center', va='center', fontsize=12,
                     bbox=dict(facecolor=color, edgecolor='black', boxstyle='circle,pad=0.5'))
            plt.text(x, y - 0.3, "w=" + str(node.weight), ha='center', va='center', fontsize=12)

        # 如果有左子节点，计算左子节点的位置并绘制线条和递归调用
        if node.left:
            new_x = x - dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.left, canonical, new_x, new_y, layer + 1, dx)

        # 如果有右子节点，计算右子节点的位置并绘制线条和递归调用
        if node.right:
            new_x = x + dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.right, canonical, new_x, new_y, layer + 1, dx)

# 主函数，初始化二叉树并可视化
def visualize_tree(root,canonical):
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    plot_tree(root,canonical)
    plt.show()

def creat_sample_y_axis_tree():
    root = TreeNode()
    dummy = root
    root.left.left = TreeNode(val=1,weight=0.25)
    root.left.right = TreeNode(val=2,weight=0.25)
    root.right.left = TreeNode(val=3, weight=0.25)
    root.right.right = TreeNode(val=4, weight=0.25)
    calculate_weight(root)
    update_intervals(root)
    return dummy

if __name__ == '__main__':
    pack_dict = {}
    times_dict = defaultdict(int)
    root = TreeNode()
    root.left = TreeNode()
    root.right = TreeNode()
    root.left.left = TreeNode()
    root.left.left.left = TreeNode(val=1, weight=0.1)
    root.left.left.right = TreeNode(val=4, weight=0.1)
    root.left.right = TreeNode()
    root.left.right.left = TreeNode(val=7, weight=0.15)
    root.left.right.right = TreeNode(val=8, weight=0.15)
    root.right.left = TreeNode()
    root.right.right = TreeNode()
    root.right.left.left = TreeNode(val = 9, weight = 0.1)
    root.right.left.right = TreeNode(val = 11, weight = 0.1)
    root.right.right.left = TreeNode(val=12, weight=0.15)
    root.right.right.right = TreeNode(val = 13, weight = 0.15)
    calculate_weight(root)
    update_internal_nodes(root)
    canonical,weights = find_paths_and_collect(root,4,12)
    visualize_tree(root,canonical)
