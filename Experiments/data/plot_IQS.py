import pandas as pd
import matplotlib.pyplot as plt

def plot_IQS_3lines(df,n,s):
    # 自定义颜色和标签
    colors = ['red', 'blue', 'green']  # 数据点的颜色
    labels = ['Tree-Traverse', 'Alias-Optimization', 'Double-Alias']  # 数据点的标签

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(df.columns[1:]):  # 遍历第二列到第四列
        plt.scatter(df[df.columns[0]], df[col], color=colors[i], label=labels[i], alpha=0.6, s = 20)

    # 添加图例、标题和坐标轴标签
    plt.legend()
    plt.title(f"Runtime N = {n}, s = {s}%")
    plt.xlabel("Selectivity")
    plt.ylabel("Runtime (s)")

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图形
    plt.show()

def plot_IQS_2lines(df,n,s):
    # 自定义颜色和标签
    colors = ['blue', 'green']  # 数据点的颜色
    labels = ['Alias-Optimization', 'Double-Alias']  # 数据点的标签

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(df.columns[2:]):  # 遍历第二列到第四列
        plt.scatter(df[df.columns[0]], df[col], color=colors[i], label=labels[i], alpha=0.6, s = 20)

    # 添加图例、标题和坐标轴标签
    plt.legend()
    plt.title(f"Runtime N = {n}, s = {s}%")
    plt.xlabel("Selectivity")
    plt.ylabel("Runtime (s)")

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图形
    plt.show()

if __name__ == "__main__":
    # 读取 CSV 文件
    file_name = 'N_50000_s_1.csv'
    df = pd.read_csv(file_name)
    n = int(file_name.split("_")[1])
    s = int(file_name.split("_")[-1][0])
    plot_IQS_2lines(df,n,s)
    plot_IQS_3lines(df,n,s)

