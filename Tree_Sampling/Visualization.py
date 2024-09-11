# 绘制二叉树的递归函数
from matplotlib import pyplot as plt
from TreeNode import TreeNode
def plot_tree(node, x=0, y=0, layer=1, dx=1):
    if node is not None:
        # 在当前节点位置绘制节点值
        plt.text(x, y, str(node.val), ha='center', va='center', fontsize=12,
                 bbox=dict(facecolor='skyblue', edgecolor='black', boxstyle='circle,pad=0.5'))

        # 如果有左子节点，计算左子节点的位置并绘制线条和递归调用
        if node.left:
            new_x = x - dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.left, new_x, new_y, layer + 1, dx)

        # 如果有右子节点，计算右子节点的位置并绘制线条和递归调用
        if node.right:
            new_x = x + dx / layer
            new_y = y - 1
            plt.plot([x, new_x], [y, new_y], 'k-')
            plot_tree(node.right, new_x, new_y, layer + 1, dx)


# 主函数，初始化二叉树并可视化
def visualize_tree(root):
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    plot_tree(root)
    plt.show()

if __name__ == '__main__':
    # 示例：构建一棵简单的二叉树
    root = TreeNode(val = 1)
    root.left = TreeNode(val = 2)
    root.right = TreeNode(val = 3)
    root.left.left = TreeNode(val = 4)
    root.left.right = TreeNode(val = 5)
    root.right.left = TreeNode(val = 6)
    root.right.right = TreeNode(val = 7)
    root.right.left.left = TreeNode(val=4)
    root.right.left.right = TreeNode(val=7)
    root.right.right.right = TreeNode(val=9)

    # 可视化二叉树
    visualize_tree(root)