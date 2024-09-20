# 绘制二叉树的递归函数
from collections import defaultdict

from matplotlib import pyplot as plt
from TreeNode import TreeNode
from Sampling import *
from Tree_Sampling.Tools import calculate_weight
from Tools import update_internal_nodes


def plot_tree(node, canonical, x=0, y=0, layer=1, dx=1):
    if node is not None:
        # 在当前节点位置绘制节点值
        if node in canonical:
            color = "red"
        else:
            color = "skyblue"
        plt.text(x, y, str(node.val), ha='center', va='center', fontsize=12,
                 bbox=dict(facecolor=color, edgecolor='black', boxstyle='circle,pad=0.5'))
        plt.text(x + 0.3, y, "w=" + str(node.weight), ha='center', va='center', fontsize=12)

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

if __name__ == '__main__':
    times_dict = defaultdict(int)
    root = TreeNode(val = 10)
    root.left = TreeNode(val = 4)
    root.right = TreeNode(val = 15)
    root.left.left = TreeNode(val = 1, weight = 0.15)
    root.left.right = TreeNode(val = 2, weight = 0.15)
    root.right.left = TreeNode(val = 6)
    root.right.right = TreeNode(val = 7)
    root.right.left.left = TreeNode(val = 3, weight = 0.2)
    root.right.left.right = TreeNode(val = 4, weight = 0.2)
    root.right.right.right = TreeNode(val = 5, weight = 0.3)
    calculate_weight(root)
    update_internal_nodes(root)
    # 可视化二叉树
    canonical,weights = find_canonical_nodes(root,1,5)
    visualize_tree(root,canonical)
    basic_sampling_preprocess(canonical,weights)
    sampled_nodes = basic_sampling(canonical,10000)
    for node in sampled_nodes:
        times_dict[leaf_sampling(node).val] += 1
    for key,value in times_dict.items():
        print(f"{key} index sampled {value} times")