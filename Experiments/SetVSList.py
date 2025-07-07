import random
import time

# 创建一个包含大量元素的列表和集合
num_elements = 1000000
data_list = list(range(num_elements))
data_set = set(range(num_elements))

# 方法1: 使用 random.sample 从列表中采样
def sample_from_list(data, sample_size):
    start_time = time.time()
    sample = random.sample(data, sample_size)
    end_time = time.time()
    return end_time - start_time

def choice_from_list(data, sample_size):
    start_time = time.time()
    res = []
    for i in range(sample_size):
        sample = random.choice(data)
        res.append(sample)
    end_time = time.time()
    return end_time - start_time

# 方法2: 使用for循环从集合中弹出元素（有放回）
def pop_from_set(data, pop_size):
    start_time = time.time()
    popped_elements = []
    for _ in range(pop_size):
        element = data.pop() if data else None  # 弹出一个元素
        if element is not None:
            popped_elements.append(element)
            data.add(element)  # 有放回
    end_time = time.time()
    return end_time - start_time

# 设置采样数量

if __name__ == "__main__":
# 测试性能
    sample_size = 30000
    list_time = sample_from_list(data_list, sample_size)
    set_time = pop_from_set(data_set.copy(), sample_size)  # 复制集合以保持原始数据不变
    list_time_2 = choice_from_list(data_list,sample_size)

    # 输出结果
    print(f"Time taken to sample {sample_size} elements from list: {list_time:.6f} seconds")
    print(f"Time taken to choice {sample_size} elements from list: {list_time_2:.6f} seconds")
    print(f"Time taken to pop {sample_size} elements from set: {set_time:.6f} seconds")