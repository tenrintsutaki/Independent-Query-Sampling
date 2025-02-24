import random
class Tester():
    def __init__(self,keys,weights,threshold):
        # 键，值，和允许结果偏差的百分量
        self.keys = keys
        self.weights = weights
        self.time_dict = {key: 0 for key in keys}
        self.s = 0
        self.THRESHOLD = threshold
        self.counter = 0
    def add_record(self,k):
        self.time_dict[k] += 1
        self.s += 1
    def valid(self):
        for k,v in self.time_dict.items():
            initial_index = self.keys.index(k)
            expected_value = self.weights[initial_index] * self.s
            if expected_value * (1 - self.THRESHOLD) <= v and expected_value * (1 + self.THRESHOLD) >= v:
                self.counter += 1
        print(f"The Validation Result is: {self.counter / len(self.keys)}")
        return self.counter / len(self.keys)

if __name__ == "__main__":
    l1 = [1,2,3,4,5]
    l2 = [0.05,0.3,0.5,0.1,0.05]
    tester = Tester(l1,l2)
    for i in range(0,1000):
        sample = random.choices(l1,weights=l2,k=1)
        tester.add_record(sample[0])
    tester.valid()