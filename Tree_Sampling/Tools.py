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