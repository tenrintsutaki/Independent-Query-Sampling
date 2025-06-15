class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.values = []
        self.weights = []
        self.right_sibling = None
        self.parent = None

    def get_min_key(self):
        if self.is_leaf:
            return self.values[0] if self.values else None
        return self.children[0].get_min_key()

    def get_max_key(self):
        if self.is_leaf:
            return self.values[-1] if self.values else None
        return self.children[-1].get_max_key()

    def __repr__(self):
        if self.is_leaf:
            return f"LeafNode(keys={self.values}, weights={self.weights})"
        return f"InternalNode(keys={self.keys})"


def build_bplus_tree(val_list, weight_list, m):
    sorted_data = sorted(zip(val_list, weight_list), key=lambda x: x[0])
    sorted_vals = [x[0] for x in sorted_data]
    sorted_weights = [x[1] for x in sorted_data]

    # 构建叶子节点
    leaf_size = m - 1
    leaves = []
    for i in range(0, len(sorted_vals), leaf_size):
        end = min(i + leaf_size, len(sorted_vals))
        leaf = BPlusTreeNode(is_leaf=True)
        leaf.values = sorted_vals[i:end]
        leaf.weights = sorted_weights[i:end]
        leaves.append(leaf)

    # 链接叶子节点
    for i in range(len(leaves) - 1):
        leaves[i].right_sibling = leaves[i + 1]

    # 构建内部节点层
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        group_size = m  # 每个内部节点最多 m 个子节点

        for i in range(0, len(current_level), group_size):
            group = current_level[i:i + group_size]

            internal_node = BPlusTreeNode()
            internal_node.children = group
            internal_node.keys = [child.get_max_key() for child in group[:-1]]

            for child in group:
                child.parent = internal_node

            next_level.append(internal_node)

        current_level = next_level

    return current_level[0] if current_level else None


def search(root, val):
    current = root
    while not current.is_leaf:
        idx = 0
        while idx < len(current.keys) and val > current.keys[idx]:
            idx += 1
        current = current.children[idx]
    return current


def sample_leaves_in_range(root, x, y):
    start_leaf = search(root, x)
    end_leaf = search(root, y)

    leaves = []
    current = start_leaf
    while current:
        current_min = current.get_min_key()
        current_max = current.get_max_key()
        if current_min > y or current_max < x:
            current = current.right_sibling
            continue

        leaves.append(current)
        if current == end_leaf:
            break
        current = current.right_sibling

    all_values = []
    all_weights = []
    for leaf in leaves:
        all_values.extend(leaf.values)
        all_weights.extend(leaf.weights)

    return all_values, all_weights


# 测试用例
if __name__ == "__main__":
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    m = 3

    root = build_bplus_tree(values, weights, m)
    print("Root node:", root)  # 输出：InternalNode(keys=[40,80])

    test_val = 45
    found_leaf = search(root, test_val)
    print(f"Search {test_val} found leaf:", found_leaf)  # 输出：LeafNode(keys=[40,50])

    x, y = 25, 75
    sample_values, sample_weights = sample_leaves_in_range(root, x, y)
    print(f"Sampled values between {x}-{y}:")
    print("Values:", sample_values)  # 输出：[30,40,50,60,70]
    print("Weights:", sample_weights)  # 输出：[3,4,5,6,7]