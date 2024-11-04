import random
import bisect
from collections import defaultdict


def weighted_sampling(weights, s):
    # 计算权重的累积和
    cumulative_weights = [0] * len(weights)
    cumulative_weights[0] = weights[0]
    for i in range(1, len(weights)):
        cumulative_weights[i] = cumulative_weights[i - 1] + weights[i]

    # 进行采样
    sampled_indices = []
    total_weight = cumulative_weights[-1]  # 权重总和
    for _ in range(s):
        # 生成一个随机数，范围在 [0, total_weight)
        rand_value = random.uniform(0, total_weight)
        # 使用二分查找找到该随机数对应的索引
        index = bisect.bisect_right(cumulative_weights, rand_value)
        sampled_indices.append(index)

    return sampled_indices

if __name__ == '__main__':
    # 示例
    weights = [10, 20, 30, 40]
    s = 1000000
    sampled_indices = weighted_sampling(weights, s)
    times_dict = defaultdict(int)
    for element in sampled_indices:
        times_dict[element] += 1
    for key,values in sorted(times_dict.items(),key = lambda x : x[1], reverse = False):
        print(key, values)