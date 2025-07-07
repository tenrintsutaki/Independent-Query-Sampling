def find_min_in_right_subtree(node):
    """帮助函数，用于找到右子树中的最小值"""
    while node.left:
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


def traverse_path(root,target,direction):
    """遍历二叉搜索树的路径，记录沿途所有的节点数据"""
    res = []
    removed = []
    weights = [1.0]
    def find_leaf_with_value(node, target, temp):
        """在二叉搜索树中查找值为target的叶子节点"""
        if not node:
            return None  # 如果节点为空，返回None

        # 如果当前节点的值等于目标值，并且是叶子节点
        if node.val == target and node.is_leaf():
            if (temp.left == node or temp.right == node):
                if temp.left == node and direction == 'L':
                    # Not the time remove the parent node
                    return node
                if temp.right == node and direction == 'R':
                    # Not the time to remove the parent node
                    return node
                # Other cases, remove the parent node and add the leaf node
                res.append(node)
                # weights.append(node.weight)
                res.remove(temp)
                removed.append(temp)
            else:
                res.append(node)
            return node

        # 情况1:target小于val，搜索左侧子树
        if target < node.val and node.left:
            if node.left.right and not node.left.right.is_leaf():
                temp = node.left.right
                res.append(temp)
                # weights.append(temp.weight)
            return find_leaf_with_value(node.left, target, temp)

        # 情况2:target大于等于val，搜索右侧子树
        elif target >= node.val and node.right:
            if node.right.left and not node.right.left.is_leaf():
                temp = node.right.left
                res.append(temp)
                # weights.append(temp.weight)
            return find_leaf_with_value(node.right, target, temp)

    find_leaf_with_value(root, target, None)
    return res,weights,removed

def find_leaves(node):
    """ find how many leaf nodes in these current input {node} """
    res = []
    def find_leaves_nodes(root):
        if root is None:
            return
        if root.is_leaf():
            res.append(root)
            return
        find_leaves_nodes(root.left)
        find_leaves_nodes(root.right)

    find_leaves_nodes(node)
    return res

def calculate_height(node):
    """calculate the height of a tree-node"""
    if not node:
        return 0
    left = calculate_height(node.left)
    right = calculate_height(node.right)
    return max(left, right) + 1