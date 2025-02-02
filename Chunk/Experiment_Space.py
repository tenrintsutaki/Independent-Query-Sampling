import sys

def calculate_tree_memory(node):
    if node is None:
        return 0

    if node.is_leaf(): # For the chunks
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
        else: # Else, they are chunks
            total_memory += calculate_chunk_memory(e)
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
