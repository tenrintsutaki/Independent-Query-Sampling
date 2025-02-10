import sys
from Chunk.builder import build_chunk
from Chunk.chunk_structure import Chunk_Structure
from Construction_Tools import *
from Sample_Tools import calculate_weight, update_internal_nodes
from Sampling import find_canonical_nodes_new, basic_sampling, leaf_sampling, find_canonical_nodes, \
    comparable_sampling, \
    find_paths_and_collect, basic_sampling_preprocess, update_intervals

from Sampling_Alias import leaf_sampling_alias, alias_sampling, alias_sampling_direct
from Experiments.Exp_Generator import generate_random_interval
from pympler import asizeof


def calculate_tree_memory(node):
    if node is None:
        return 0

    if isinstance(node,Chunk_Structure): # For the chunks
        return calculate_chunk_memory(node)

    # Memory for the current node object itself
    total_memory = sys.getsizeof(node)

    # Memory for each attribute of the node
    total_memory += sys.getsizeof(node.l_val)
    total_memory += sys.getsizeof(node.r_val)
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
    for e in AS.elements:
        if (isinstance(e, int)): # When the element in the AS is int
            total_memory += sys.getsizeof(e)
        elif (isinstance(e, Chunk_Structure)): # Else, they are chunks
            total_memory += calculate_chunk_memory(e)
        else:
            raise Exception("Wrong Type in AS Elements")
    return total_memory

def calculate_chunk_memory(chunk):
    if chunk is None:
        return 0
    total_memory = sys.getsizeof(chunk)
    total_memory += sys.getsizeof(chunk.l_val)
    total_memory += sys.getsizeof(chunk.r_val)
    total_memory += sys.getsizeof(chunk.weight)
    total_memory += sys.getsizeof(chunk.left)
    total_memory += sys.getsizeof(chunk.right)
    total_memory += sys.getsizeof(chunk.raw)
    for e in chunk.raw:
        total_memory += sys.getsizeof(e)
    total_memory += calculate_as_memory(chunk.AS)
    return total_memory

def build_test_tree(num_nodes,chunk_size):
    random_list = random_tree_assigned(num_nodes)
    weights = generate_random_weights(num_nodes)
    chunk_list = build_chunk(random_list, weights, chunk_size)
    root, leaf_index = construct_bst(chunk_list, weights)  # 写一下
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root)  # BUILD AS
    res = asizeof.asizeof(root)/ (1024 * 1024 * 1024)
    print(f"Measured by asizeof:{res} with {num_nodes} nodes")  # 输出字节数
    return res

if __name__ == '__main__':
    result = []

    num_nodes = [i for i in range(0,4000000 + 1,250000)]

    chunk_size = 1000

    for n in num_nodes:
        result.append(build_test_tree(n,chunk_size))

    with open(f'../Result/chunk_result_{chunk_size}.txt', 'w') as file:
        i = 0
        for item in result:
            file.write(f"{num_nodes[i]},{item}\n")  # 每个元素写入一行
            i += 1
