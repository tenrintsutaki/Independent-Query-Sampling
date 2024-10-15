import time
from collections import defaultdict
import random

from Alias_Structure import AliasStructure

def test_alias_structure(probs,times):
    start = time.time()
    times_dict = defaultdict(int)
    alias_structure = AliasStructure(probs)
    alias_structure.initialize()
    end = time.time()
    print(f'Time consume {end - start} to build')
    for i in range(times):
        result = alias_structure.sample()
        times_dict[result] += 1
    ls = sorted(times_dict.items(), key=lambda x: x[0])
    for v in ls:
        print(f"{v[0]} index sampled {v[1]} times")

def test_alias_structure_old(probs,times):
    start = time.time()
    times_dict = defaultdict(int)
    alias_structure = AliasStructure(probs)
    alias_structure.initialize_old()
    end = time.time()
    print(f'Time consume {end - start} to build (old)')
    for i in range(times):
        result = alias_structure.sample()
        times_dict[result] += 1
    ls = sorted(times_dict.items(), key=lambda x: x[0])



if __name__ == '__main__':
    dice_list = [10,20,30,40]
    s = sum(dice_list)
    for i in range(len(dice_list)):
        dice_list[i] = dice_list[i] / s
    test_alias_structure(dice_list, 100000)

    # dice_list = [random.randint(0, 2000) for _ in range(2000000)]



    # test_alias_structure(dice_list, 1000)
    # test_alias_structure_old(dice_list, 1000)
    # For tree sampling, we could use the alias_structure in each node and store its leaf nodes

