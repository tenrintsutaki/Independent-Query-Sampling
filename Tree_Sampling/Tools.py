def find_min_in_right_subtree(node):
    """帮助函数，用于找到右子树中的最小值"""
    if not node:
        return float('inf')  # 如果节点为空，返回无穷大
    while node.left:  # 迭代到最左边的节点
        node = node.left
    return node.val

def update_internal_nodes(node):
    """递归更新内部节点的值"""
    if not node:
        return

    # 先更新右子树
    update_internal_nodes(node.right)

    # 处理左子树
    update_internal_nodes(node.left)

    # 如果当前节点是内部节点（有右子树），则更新值
    if node.right:
        node.val = find_min_in_right_subtree(node.right)

def calculate_weight(root):
    if not root:
        return 0
    # Post - Order Traverse
    left_weight = calculate_weight(root.left)
    right_weight = calculate_weight(root.right)
    root.weight = left_weight + right_weight + root.weight # Calculate the weight
    return root.weight


def traverse_path(root,target):
    """遍历二叉搜索树的路径，记录沿途所有的节点数据"""
    res = [root]
    def find_leaf_with_value(node, target):
        """在二叉搜索树中查找值为target的叶子节点"""
        if not node:
            return None  # 如果节点为空，返回None

        # 如果当前节点的值等于目标值，并且是叶子节点
        if node.val == target and not node.left and not node.right:
            return node

        # 情况1:target小于val，搜索左侧子树
        if target < node.val:
            if(node.left):
                res.append(node.left)
            return find_leaf_with_value(node.left, target)
        # 情况2:target大于等于val，搜索右侧子树
        else:
            if(node.right):
                res.append(node.right)
            return find_leaf_with_value(node.right, target)
    find_leaf_with_value(root, target)
    return res

