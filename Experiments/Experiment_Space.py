import sys

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

    return total_memory