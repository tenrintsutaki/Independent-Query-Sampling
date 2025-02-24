import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


# 读取文件a.txt和b.txt
def read_file(filename):
    x_values = []
    y_values = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = line.strip().split(',')
            x_values.append(float(x))
            y_values.append(float(y))
    return x_values, y_values

# 读取a.txt和b.txt的数据
x_a, y_a = read_file('chunk_result_100.txt')
x_b, y_b = read_file('normal_result.txt')
plt.figure(figsize=(10,5))
# 绘制折线图
plt.plot(x_a, y_a, label='Chunk', marker='o',color = 'orange')
plt.plot(x_b, y_b, label='Normal', marker='s',color = 'blue')


# 添加标题和标签
plt.title('Memory Comparison of Chunk and Normal Structure')
plt.xlabel('Data Set Size')
plt.ylabel('Memory Overhead (GB)')
plt.grid(True)

plt.gca().xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
plt.ticklabel_format(style='plain', axis='x')  # 确保x轴不使用科学计数法
# 添加图例
plt.legend()


# 显示图形
plt.show()