import time
from collections import defaultdict
import random
from Alias.Alias_Structure import AliasStructure
from Tree_Sampling.Python_Sample import weighted_sampling

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


if __name__ == '__main__':
    weights = [10,10,10,10,10,50]
    dic = defaultdict(int)
    index = weighted_sampling(weights,100000)
    for i in index:
        dic[i] += 1
    for key,value in sorted(dic.items(),key=lambda x:x[1]):
        print(key,value)
    # weights = [random.randint(1, 999) for _ in range(50000)]
    # for i in range(len(weights)):
    #     weights[i] = weights[i] / sum(weights)
    #
    # s = 10 ** 8 # 1 Billion
    # start = time.time()
    # weighted_sampling(weights, s)
    # end = time.time()
    # print(f'Time consume {end - start} to use Normal')
    #
    # start = time.time()
    # test_alias_structure(weights, s)
    # end = time.time()
    # print(f'Time consume {end - start} to use AS')





