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

if __name__ == "__main__":
    n = 1000
    val_list = [random.randint(0,100000) for _ in range(n)]
    weight_list = [random.randint(0, 100000) for _ in range(n)]
    val_list.sort()
    for i in range(n):
        weight_list[i] = weight_list[i] / sum(weight_list)
    chunk_list = build_chunk(val_list,weight_list,10) # Build Chunk List



