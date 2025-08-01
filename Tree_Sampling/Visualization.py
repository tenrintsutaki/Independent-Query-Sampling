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

    # path = traverse_path(root,1)
    # for node in path:
    #     print(node.val, node.weight)
    # 可视化二叉树
    tester = Tester([1,4,7,8,9,11,12,13],[0.1,0.1,0.15,0.15,0.1,0.1,0.15,0.15],0.1)
    canonical,weights = find_paths_and_collect(root,1,8)
    print(canonical)
    visualize_tree(root,canonical)

    print(f"Measure by asizeof: {asizeof.asizeof(root)}")
    print(f"Measure by Tenrin: {calculate_tree_memory(root)}")

    basic_sampling_preprocess(canonical,weights)
    update_intervals(root)
    sampled_nodes = basic_sampling(canonical,10000)
    for node in sampled_nodes:
        res = leaf_sampling(node).val
        times_dict[res] += 1
        tester.add_record(res)
    for key,value in times_dict.items():
        print(f"{key} index sampled {value} times")
    tester.valid()
    # print(calculate_leaf_numbers(canonical))
    # print(root.interval)
    #
    # compare_list = comparable_sampling(root,4,9)
    # for node in compare_list:
    #     print("Compare path:",node.val)
    # res = find_leaves(root)
    # for node in res:
    #     print("Leaves:",node.val)
    # print(f"height: {calculate_height(root)}")