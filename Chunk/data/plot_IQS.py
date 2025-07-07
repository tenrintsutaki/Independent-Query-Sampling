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
    plt.title(f"Runtime N = {n}, s = {s}")
    plt.xlabel("Selectivity")
    plt.ylabel("Runtime (s)")

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图形
    plt.savefig(f"images/N_{n}_s_{s}_3lines.png", dpi=300, bbox_inches="tight")  # 保存为 PNG 文件
    plt.show()


def plot_IQS_2lines(df,n,s):
    # if (len(s) == 2):
    #     s = s[0] + "." + s[1]
    # 自定义颜色和标签
    colors = ['blue', 'green']  # 数据点的颜色
    labels = ['Alias-Optimization', 'Double-Alias']  # 数据点的标签

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(df.columns[1:]):  # 遍历第二列到第四列
        plt.scatter(df[df.columns[0]], df[col], color=colors[i], label=labels[i], alpha=0.6, s = 20)

    # 添加图例、标题和坐标轴标签
    plt.legend()
    plt.title(f"Runtime N = {n}, s = {s}")
    plt.xlabel("Selectivity")
    plt.ylabel("Runtime (s)")

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图形
    plt.savefig(f"images/N_{n}_s_{s}_2lines.png", dpi=300, bbox_inches="tight")  # 保存为 PNG 文件
    plt.show()

def plot_IQS_4lines(df_chunk,df_normal,n,s):
    # 自定义颜色和标签
    colors = ['blue', 'green','orange','red']  # 数据点的颜色
    labels = ['Alias-Optimization (Chunk)', 'Double-Alias (Chunk)','Alias-Optimization', 'Double-Alias']  # 数据点的标签

    # 绘制散点图
    # plt.figure(figsize=(8, 6))
    # for i, col in enumerate(df_chunk.columns[1:2]):  # 遍历第二列到第四列
    #     plt.scatter(df_chunk[df_chunk.columns[0]], df_chunk[col], color='red', label=labels[0], alpha=0.6, s = 20)
    #
    # for i, col in enumerate(df_normal.columns[2:3]):  # 遍历第二列到第四列
    #     plt.scatter(df_normal[df_normal.columns[0]], df_normal[col], color='orange', label=labels[2], alpha=0.6, s = 20)
    #
    # # 添加图例、标题和坐标轴标签
    # plt.legend()
    # plt.title(f"Runtime N = {n}, s = {s}")
    # plt.xlabel("Selectivity")
    # plt.ylabel("Runtime (s)")
    #
    # # 显示网格
    # plt.grid(True, linestyle='--', alpha=0.7)
    #
    # # 显示图形
    # plt.savefig(f"images/N_{n}_s_{s}_2lines.png", dpi=300, bbox_inches="tight")  # 保存为 PNG 文件
    # plt.show()

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    for i, col in enumerate(df_chunk.columns[2:3]):  # 遍历第二列到第四列
        plt.scatter(df_chunk[df_chunk.columns[0]], df_chunk[col], color='red', label=labels[1], alpha=0.7, s=20)

    for i, col in enumerate(df_normal.columns[3:4]):  # 遍历第二列到第四列
        plt.scatter(df_normal[df_normal.columns[0]], df_normal[col], color='orange', label=labels[3], alpha=0.7,
                    s=20)

    # 添加图例、标题和坐标轴标签
    plt.legend()
    plt.title(f"Runtime N = {n}, s = {s}")
    plt.xlabel("Selectivity")
    plt.ylabel("Runtime (s)")

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图形
    plt.savefig(f"images/N_{n}_s_{s}_2lines.png", dpi=300, bbox_inches="tight")  # 保存为 PNG 文件
    plt.show()

if __name__ == "__main__":
    # 读取 CSV 文件
    s = 1000
    n = 250000
    file_name = f'N_{n}_s_{s}_chunk_100.csv'
    file_name_2 = f'N_{n}_s_{s}_.csv'
    df = pd.read_csv(file_name)
    df2 = pd.read_csv(file_name_2)
    n = int(file_name.split("_")[1])
    s = int(file_name.split("_")[3])
    plot_IQS_4lines(df,df2,n,s)
#   plot_IQS_3lines(df,n,s)

