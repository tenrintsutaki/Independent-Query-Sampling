import random
import numpy as np
from scipy.stats import chisquare
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
        self.result_factors = []
        self.ex_dict = {}
    def add_record(self,k):
        self.time_dict[k] += 1
        self.s += 1
    def valid(self):
        self.__remove_zeros_normalize()
        for k,v in self.time_dict.items():
            initial_index = self.keys.index(k)
            expected_value = self.sample_weights[initial_index] * self.s
            self.ex_dict[k] = expected_value
            if expected_value * (1 - self.THRESHOLD) <= v and expected_value * (1 + self.THRESHOLD) >= v:
                self.counter += 1
            if expected_value != 0:
                self.result_factors.append(v / expected_value)
        print(f"The Validation Result is: {self.counter / len(self.keys)}")
        return self.result_factors
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

    # def get_standard_validation_diagram(self):

    def chi_square_validation(self):
        observed = []
        expected = []
        for k in self.time_dict.keys():
            observed.append(self.time_dict[k])
            expected.append(self.ex_dict[k])
        chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
        print(f"Chi_Square: {chi2_stat:.4f}")
        print(f"P: {p_value:.4f}")

        # 判断显著性（α=0.05）
        alpha = 0.05
        if p_value < alpha:
            print("Rejection of the original hypothesis: frequency of observations is significantly different from theoretical expectations (possible problems with the algorithm))")
        else:
            print("Accept of the original hypothesis: frequency of observations is consistent with theoretical expectations (algorithm passes the test)")
        return p_value

if __name__ == "__main__":
    l1 = [1,2,3,4,5]
    l2 = [0.05,0.3,0.5,0.1,0.05]
    tester = Tester(l1,l2)
    for i in range(0,1000):
        sample = random.choices(l1,weights=l2,k=1)
        tester.add_record(sample[0])
    tester.valid()