import sys
from Tree_Sampling.Construction_Tools import *
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from pympler import asizeof

def calculate_tree_memory(node):
    if node is None:
        return 0

    # Memory for the current node object itself
    total_memory = sys.getsizeof(node)

    # Memory for each attribute of the node
    total_memory += sys.getsizeof(node.val)
    total_memory += sys.getsizeof(node.weight)
    total_memory += sys.getsizeof(node.left)
    total_memory += sys.getsizeof(node.right)
    total_memory += calculate_as_memory(node.AS)

    # Recursively calculate the memory of the left and right subtrees
    total_memory += calculate_tree_memory(node.left)
    total_memory += calculate_tree_memory(node.right)
    return total_memory

def calculate_urn_memory(urn):
    if urn is None:
        return 0
    total_memory = sys.getsizeof(urn)
    total_memory += sys.getsizeof(urn.count)
    total_memory += sys.getsizeof(urn.e1)
    total_memory += sys.getsizeof(urn.i1)
    total_memory += sys.getsizeof(urn.e2)
    total_memory += sys.getsizeof(urn.i2)
    return total_memory

def calculate_as_memory(AS):
    if AS is None:
        return 0
    total_memory = sys.getsizeof(AS)
    total_memory += sys.getsizeof(AS.avg)

    total_memory += sys.getsizeof(AS.probs)
    for e in AS.probs:
        total_memory +=  sys.getsizeof(e)

    total_memory += sys.getsizeof(AS.UrnSet)
    for urn in AS.UrnSet:
        total_memory += calculate_urn_memory(urn)

    total_memory += sys.getsizeof(AS.e1List)
    for e in AS.e1List:
        total_memory +=  sys.getsizeof(e)

    total_memory += sys.getsizeof(AS.e2List)
    for e in AS.e2List:
        total_memory +=  sys.getsizeof(e)

    total_memory += sys.getsizeof(AS.avgList)
    for e in AS.avgList:
        total_memory +=  sys.getsizeof(e)

    total_memory += sys.getsizeof(AS.elements)
    if AS.elements:
        for e in AS.elements:
            total_memory += sys.getsizeof(e)

    return total_memory

def build_test_tree(num_nodes):
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    root, leaf_index = construct_bst(random_list, weights, 0)  # 写一下
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root)  # BUILD AS
    res = calculate_tree_memory(root) / (1024 * 1024 * 1024)
    print(f"Measured by asizeof:{res} with {num_nodes} nodes")  # 输出字节数
    return res

if __name__ == '__main__':
    result = []

    num_nodes = [i for i in range(0,4000000 + 1,250000)]

    for n in num_nodes:
        result.append(build_test_tree(n))

    with open(f'../Result/normal_result.txt', 'a') as file:
        i = 0
        for item in result:
            file.write(f"{num_nodes[i]},{item}\n")  # 每个元素写入一行
            i += 1