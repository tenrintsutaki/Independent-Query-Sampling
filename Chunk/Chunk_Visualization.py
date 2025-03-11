# 绘制二叉树的递归函数
import random
from collections import defaultdict

from matplotlib import pyplot as plt
from TreeNode import TreeNode
from Sampling import *
from Sample_Tools import update_internal_nodes,traverse_path,calculate_weight,find_leaves,calculate_height
from Tree_Sampling.Construction_Tools import calculate_leaf_numbers
from Validation.Result_Tester import Tester
from builder import build_chunk, replace_non_align_chunk
from Sampling_Alias import leaf_sampling_alias
from Construction_Tools import build_AS_structure
from pympler import asizeof
from Experiment_Space import *

#TODO: 之前的sample没有获取到Value元素
def plot_tree(node, canonical, left, right, x=0, y=0, layer=1, dx=1):
    if node is not None:
        # 在当前节点位置绘制节点值
        if node in canonical:
            color = "orange"
        else:
            color = "skyblue"
        if not left and node == canonical[-2]:
            color = "red"
        if not right and node == canonical[-1]:
            color = "red"
        plt.text(x, y, str(str(node.l_val) + "," + str(node.r_val)), ha='center', va='center', fontsize=12,
                 bbox=dict(facecolor=color, edgecolor='black', boxstyle='circle,pad=0.5'))
        # plt.text(x + 0.3, y, "w=" + str(node.weight), ha='center', va='center', fontsize=12)

        # 如果有左子节点，计算左子节点的位置并绘制线条和递归调用
        if node.left:
            new_x = x - dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.left, canonical, left, right, new_x, new_y, layer + 1, dx)

        # 如果有右子节点，计算右子节点的位置并绘制线条和递归调用
        if node.right:
            new_x = x + dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.right, canonical, left, right, new_x, new_y, layer + 1, dx)

# 主函数，初始化二叉树并可视化
def visualize_tree(root,canonical,l_align,r_align):
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    plot_tree(root,canonical,l_align,r_align)
    plt.show()

if __name__ == '__main__':
    times_dict = defaultdict(int)
    leaf_count = 80
    chunk_size = 10
    x = 1
    y = 80
    k = 200000

    val_list = [x for x in range(1,leaf_count+1)]
    weight_list = [random.randint(1,100) for _ in range(1,leaf_count+1)]
    for i in range(len(weight_list)):
        weight_list[i] = weight_list[i] / sum(weight_list)
    chunk_list = build_chunk(val_list,weight_list,chunk_size)
    tester = Tester(val_list,weight_list,0.1)

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
    canonical,weights,l_align,r_align = find_paths_and_collect(root,x,y)
    # visualize_tree(root,canonical,l_align,r_align)

    #把末尾两个canonical变化一下
    # [-1]为最后一个chunk, [-2]为第一个chunk
    canonical = replace_non_align_chunk(canonical,l_align,r_align,x,y)
    basic_sampling_preprocess(canonical,weights)
    build_AS_structure(root)  # BUILD AS
    result = basic_sampling(canonical, k) # Sample a canonical node firstly using basic sample
    set_result = set(result)
    for node in result:
        sampled_chunk = leaf_sampling_alias(node) # Then use alias sampling to get the result\
        res = sampled_chunk.AS.sample_element()
        tester.add_record(res)
    c = chunk_list[0]
    # print(f"Measure by asizeof: {asizeof.asizeof(c.AS)}")
    # print(f"Measure by Tenrin: {calculate_as_memory(c.AS)}")
    result_factors = tester.valid()
    plt.figure(figsize=(10, 6))
    plt.axhline(y=1, color='red', linestyle='-')
    plt.ylim(0,2)
    plt.scatter([i for i in range(len(result_factors))],result_factors)
    p_value = tester.chi_square_validation()
    plt.title(f"Validation with p = {p_value}")
    plt.show()
