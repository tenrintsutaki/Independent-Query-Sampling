# 绘制二叉树的递归函数
import random
from collections import defaultdict

from matplotlib import pyplot as plt
from TreeNode import TreeNode
from Sampling import *
from Sample_Tools import update_internal_nodes,traverse_path,calculate_weight,find_leaves,calculate_height
from Tree_Sampling.Construction_Tools import calculate_leaf_numbers
from builder import build_chunk
from Sampling_Alias import leaf_sampling_alias
from Construction_Tools import build_AS_structure

#TODO: 之前的sample没有获取到Value元素
def plot_tree(node, canonical, x=0, y=0, layer=1, dx=1):
    if node is not None:
        # 在当前节点位置绘制节点值
        if node in canonical:
            color = "orange"
        else:
            color = "skyblue"
        plt.text(x, y, str(str(node.l_val) + "," + str(node.r_val)), ha='center', va='center', fontsize=12,
                 bbox=dict(facecolor=color, edgecolor='black', boxstyle='circle,pad=0.5'))
        # plt.text(x + 0.3, y, "w=" + str(node.weight), ha='center', va='center', fontsize=12)

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
    leaf_count = 80
    chunk_size = 10
    x = 1
    y = 40
    k = 100
    val_list = [x for x in range(1,leaf_count+1)]
    weight_list = [random.randint(1,100) for _ in range(1,leaf_count+1)]
    for i in range(len(weight_list)):
        weight_list[i] = weight_list[i] / sum(weight_list)
    chunk_list = build_chunk(val_list,weight_list,chunk_size)

    root = TreeNode()
    root.left = TreeNode()
    root.right = TreeNode()
    root.left.left = TreeNode()
    root.left.left.left = chunk_list[0]
    root.left.left.right = chunk_list[1]
    root.left.right = TreeNode()
    root.left.right.left = chunk_list[2]
    root.left.right.right = chunk_list[3]
    root.right.left = TreeNode()
    root.right.right = TreeNode()
    root.right.left.left = chunk_list[4]
    root.right.left.right = chunk_list[5]
    root.right.right.left = chunk_list[6]
    root.right.right.right = chunk_list[7]
    calculate_weight(root)
    update_internal_nodes(root)
    canonical,weights = find_paths_and_collect(root,x,y)
    print(canonical)
    visualize_tree(root,canonical)

    basic_sampling_preprocess(canonical,weights)
    build_AS_structure(root)  # BUILD AS
    result = basic_sampling(canonical, k) # Sample a canonical node firstly using basic sample
    for node in result:
        sampled_chunk = leaf_sampling_alias(node) # Then use alias sampling to get the result\
        print(sampled_chunk.AS.sample())