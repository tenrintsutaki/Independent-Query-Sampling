import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


if __name__ == '__main__':
    # 模拟参数
    np.random.seed(42)
    k_values = np.arange(1, 501)  # 采样次数 k，从1到500
    v_true = 0  # 假设真实值 v' = 0

    # 模拟 v 的采样结果，随着 k 增加，波动逐渐减少
    v_samples = np.cumsum(np.random.randn(len(k_values))) / k_values

    # 计算标准误差（假设标准误差随着 k 增加而减小）
    std_errors = 1 / np.sqrt(k_values)
    print(norm.ppf(0.975))
    # 95% 置信区间的上下界
    ci_upper = v_samples + 1.96 * std_errors
    ci_lower = v_samples - 1.96 * std_errors

    # 绘制均值和置信区间
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, v_samples, label="$v_k$", color='blue')
    plt.fill_between(k_values, ci_lower, ci_upper, color='lightblue', alpha=0.5, label="95% Confidential Interval")

    # 绘制真实值线
    plt.axhline(v_true, color='red', linestyle='--', label="$v'$")

    # 图形细节
    plt.title("k and $v_k$ with 95% confidence interval")
    plt.xlabel("k")
    plt.ylabel("$v_k$")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()