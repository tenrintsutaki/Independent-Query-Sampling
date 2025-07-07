import random

from chunk_structure import Chunk_Structure
from Alias.Alias_Structure import AliasStructure

# chunk builder, using int list to construct the AS

def build_chunk(val_list,weight_list,chunk_size):
    chunk_list = []
    if len(val_list) != len(weight_list):
        raise ValueError("Length of val_list and weight_list must be same")
    if len(val_list) % chunk_size == 0:
        for i in range(0,len(val_list),chunk_size):
            chunk = Chunk_Structure(raw = val_list[i:i+chunk_size],weight = sum(weight_list[i:i+chunk_size]))
            chunk.initialize()
            as_structure = AliasStructure(probs = weight_list[i:i+chunk_size]) # Create AS
            as_structure.elements = val_list[i:i+chunk_size]
            as_structure.initialize()
            chunk.AS = as_structure # Bind AS
            chunk_list.append(chunk)
    else: # Problem 1
        # TODO: solve the problem when the size of list cannot be "mod" by the chunk_size
        pass
    return chunk_list

def build_single_chunk(val_list,weight_list):
    chunk = Chunk_Structure(raw = val_list,weight = sum(weight_list))
    chunk.initialize()
    as_structure = AliasStructure(probs = weight_list) # Create AS
    as_structure.elements = val_list
    as_structure.initialize()
    chunk.AS = as_structure # Bind AS
    return chunk

def replace_non_align_chunk(canonical,l_align,r_align,x,y):
    if (not l_align):
        left_chunk = canonical[-2]
        probs = left_chunk.AS.probs
        elements = left_chunk.AS.elements
        x_location = elements.index(x)
        canonical[-2] = build_single_chunk(elements[x_location:],probs[x_location:]) # 截取x_location之后的部分

    if (not r_align):
        right_chunk = canonical[-1]
        probs = right_chunk.AS.probs
        elements = right_chunk.AS.elements
        y_location = elements.index(y)
        canonical[-1] = build_single_chunk(elements[:y_location + 1], probs[:y_location + 1])  # 截取y_location之后的部分

    return canonical

if __name__ == "__main__":
    n = 1000
    val_list = [random.randint(0,100000) for _ in range(n)]
    weight_list = [random.randint(0, 100000) for _ in range(n)]
    val_list.sort()
    for i in range(n):
        weight_list[i] = weight_list[i] / sum(weight_list)
    chunk_list = build_chunk(val_list,weight_list,10) # Build Chunk List



