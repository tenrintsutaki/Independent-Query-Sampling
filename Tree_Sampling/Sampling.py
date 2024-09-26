import random
from Tree_Sampling.Sample_Tools import traverse_path
def find_canonical_nodes(root, x, y): # 添加Search Key
    # Find the left path and the right path......
    # 左拐和右拐的情况
    # Data Size - 1GB
    canonical_nodes = []
    weights = []
    # 递归函数来遍历树，返回是否子树的所有叶子节点都属于Canonical节点
    def dfs(node):
        if not node:
            return True  # 空节点视作满足条件

        # 叶子节点：没有左右子节点
        if not node.left and not node.right: # 待修改，加速
            if x <= node.val <= y:
                canonical_nodes.append(node)
                weights.append(node.weight)
                return True  # 叶子节点满足条件
            else:
                return False  # 叶子节点不满足条件

        # 对左右子树递归
        left_canonical = dfs(node.left)
        right_canonical = dfs(node.right)

        # 如果左右子树的叶子节点都属于Canonical节点，那么当前节点也是Canonical节点
        # Remove the right and left children after add their parent
        if left_canonical and right_canonical:
            canonical_nodes.append(node)
            if node.left: # 去除子节点，避免重复的情况
                canonical_nodes.remove(node.left)
            if node.right:
                canonical_nodes.remove(node.right)
            weights.append(node.weight)
            return True  # 当前节点也满足条件
        else:
            return False  # 当前节点不满足条件

    # 从根节点开始DFS
    dfs(root)

    return canonical_nodes,weights

def basic_sampling_preprocess(canonical_nodes,weights):
    for node in canonical_nodes: # Normalize the sample weight
        node.sample_weight = node.weight / weights

def basic_sampling(canonical_nodes,times):
    # canonical_nodes:[node 1,node 2,node 3,...,node n]
    # weights: [w1,w2,w3,w4]
    prob_list = []

    for i in range(len(canonical_nodes)):
            prob_list.append(canonical_nodes[i].weight)
    sample = random.choices(canonical_nodes, weights=prob_list, k=times)  # 根据权重进行随机采样
    return sample  # Return sampled value

def leaf_sampling(node):
    if node.is_leaf():
        return node
    if not node.left:
        return leaf_sampling(node.right)
    if not node.right:
        return leaf_sampling(node.left)
    selected_child = random.choices([node.left, node.right], weights=[node.left.weight, node.right.weight], k=1)[0]
    return leaf_sampling(selected_child)

def find_canonical_nodes_new(root,x,y):
    """Updated methods for finding canonical nodes"""
    nodes_left,weights_left,removed_left = traverse_path(root,x,"L")
    nodes_right,weights_right,removed_right = traverse_path(root,y,"R")

    nodes_left.extend(nodes_right)
    weights_left.extend(weights_right)
    removed_left.extend(removed_right)

    # nodes_left.remove(removed_left)
    for node in removed_left:# Remove the node that not been removed in a new direction
        if node in nodes_left:
            nodes_left.remove(node)

    return nodes_left, weights_left


def find_path(root, target):
    path = []
    current = root

    while current:
        path.append(current)

        if target < current.val:
            current = current.left
        elif target >= current.val:
            current = current.right

    return path  # 确保目标节点存在


def collect_nodes(root, path_x, path_y):
    collected_nodes = []
    sum_weight = 0.0
    # 找到分叉节点
    split_node = root
    for x, y in zip(path_x, path_y):
        if x == y:
            split_node = x
        else:
            break
    # get the split node.
    index_split_x = path_x.index(split_node)
    index_split_y = path_y.index(split_node)

    pre = path_x[index_split_x + 1]
    for i in range(index_split_x + 2,len(path_x)):
        if (pre.left == path_x[i]):
            collected_nodes.append(pre.right)
            sum_weight += pre.right.weight
        pre = path_x[i]

    pre = path_y[index_split_y + 1]
    for i in range(index_split_y + 2,len(path_y)):
        if (pre.right == path_y[i]):
            collected_nodes.append(pre.left)
            sum_weight += pre.left.weight
        pre = path_y[i]
    # Process the leaf node
    collected_nodes.append(path_x[-1])
    collected_nodes.append(path_y[-1])
    sum_weight += path_x[-1].weight
    sum_weight += path_y[-1].weight
    return collected_nodes,sum_weight


def find_paths_and_collect(root, x, y):
    path_x = find_path(root, x)
    path_y = find_path(root, y)

    # for node in path_x:
    #     print(f"Node in path x: {node.val}")
    #
    # for node in path_y:
    #     print(f"Node in path y: {node.val}")

    if path_x is None or path_y is None:
        return []  # 如果没有找到任何路径，返回空列表

    # 收集节点
    collected_nodes,sum_weights = collect_nodes(root, path_x, path_y)
    # print(f"collected: ",collected_nodes)
    return collected_nodes,sum_weights