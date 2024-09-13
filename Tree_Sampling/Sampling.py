import random

from TreeNode import TreeNode

def calculate_weight(root):
    if not root:
        return 0
    # Post - Order Traverse
    left_weight = calculate_weight(root.left)
    right_weight = calculate_weight(root.right)
    root.weight = left_weight + right_weight + root.weight # Calculate the weight
    return root.weight

def find_canonical_nodes(root, x, y):
    canonical_nodes = []
    weights = []

    # 递归函数来遍历树，返回是否子树的所有叶子节点都属于Canonical节点
    def dfs(node):
        if not node:
            return True  # 空节点视作满足条件

        # 叶子节点：没有左右子节点
        if not node.left and not node.right:
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
            if node.left:
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
    sum_weight = sum(weights)
    for node in canonical_nodes: # Normalize the sample weight
        node.sample_weight = node.weight / sum_weight

def basic_sampling(canonical_nodes,times):
    # canonical_nodes:[node 1,node 2,node 3,...,node n]
    # weights: [w1,w2,w3,w4]
    prob_list = []

    for i in range(len(canonical_nodes)):
            prob_list.append(canonical_nodes[i].weight)
    sample = random.choices(canonical_nodes, weights=prob_list, k=times)  # 根据权重进行随机采样
    return sample  # Return sampled value

def leaf_sampling(node):
    if not node.left and not node.right:
        return node
    if not node.left:
        return leaf_sampling(node.right)
    if not node.right:
        return leaf_sampling(node.left)
    selected_child = random.choices([node.left, node.right], weights=[node.left.weight, node.right.weight], k=1)[0]
    return leaf_sampling(selected_child)