from collections import defaultdict

from Alias_Structure import AliasStructure

def test_alias_structure(probs,times):
    times_dict = defaultdict(int)
    alias_structure = AliasStructure(probs)
    alias_structure.initialize()
    for i in range(times):
        result = alias_structure.sample()
        times_dict[result] += 1
    ls = sorted(times_dict.items(), key=lambda x: x[0])
    for v in ls:
        print(f"{v[0]} index sampled {v[1]} times")

if __name__ == '__main__':
    # dice_list = [3 / 10, 2 / 10, 2 / 10, 2 / 10, 1 / 10]
    # test_alias_structure(dice_list, 1000000)
    dice_list = [10,40]
    s = sum(dice_list)
    for i in range(len(dice_list)):
        dice_list[i] = dice_list[i] / s

    test_alias_structure(dice_list, 1000000)
    # For tree sampling, we could use the alias_structure in each node and store its leaf nodes

