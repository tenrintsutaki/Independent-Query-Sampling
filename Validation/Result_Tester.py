import random
class Tester():
    def __init__(self,keys,weights,threshold):
        # 键，值，和允许结果偏差的百分量
        self.keys = keys
        self.weights = weights
        self.sample_weights = weights
        self.time_dict = {key: 0 for key in keys}
        self.s = 0
        self.THRESHOLD = threshold
        self.counter = 0
    def add_record(self,k):
        self.time_dict[k] += 1
        self.s += 1
    def valid(self):
        self.__remove_zeros_normalize()
        for k,v in self.time_dict.items():
            initial_index = self.keys.index(k)
            expected_value = self.sample_weights[initial_index] * self.s
            if expected_value * (1 - self.THRESHOLD) <= v and expected_value * (1 + self.THRESHOLD) >= v:
                self.counter += 1
        print(f"The Validation Result is: {self.counter / len(self.keys)}")
        return self.counter / len(self.keys)
    def __remove_zeros_normalize(self):
        for k,v in self.time_dict.items():
            # 一次没有被采样的k定义为out of the range.
            if v == 0:
                self.sample_weights[self.keys.index(k)] = 0
                # 使得sample weight里面这个k的位置的权重归0
        origin_sum = sum(self.sample_weights)
        for i in range(len(self.sample_weights)):
            self.sample_weights[i] = self.sample_weights[i] / origin_sum
            # 权重逐个归一化


if __name__ == "__main__":
    l1 = [1,2,3,4,5]
    l2 = [0.05,0.3,0.5,0.1,0.05]
    tester = Tester(l1,l2)
    for i in range(0,1000):
        sample = random.choices(l1,weights=l2,k=1)
        tester.add_record(sample[0])
    tester.valid()