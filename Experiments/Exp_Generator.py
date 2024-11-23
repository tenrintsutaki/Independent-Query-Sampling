import random
import matplotlib.pyplot as plt
import numpy as np

def generate_random_interval(selectivity,total_len):
    """
    generate the random interval from the total len
    :param total_len: total_len
    :return:
    """
    # 计算区间的长度
    interval_length = int(total_len * selectivity)

    # 确保 interval_length 至少为 1
    if interval_length < 1:
        raise ValueError("Interval length must be at least 1 based on selectivity and total_len.")

    # 随机选择 start
    start = random.randint(0, total_len - interval_length - 1)  # 确保 end 不超过 total_len
    end = start + interval_length  # 计算 end

    return start, end


if __name__ == '__main__':
    res = []
    total_len = 1000000
    for i in range(100000):
        selectivity = random.random()
        start, end = generate_random_interval(selectivity,total_len)
        print(start, end)


