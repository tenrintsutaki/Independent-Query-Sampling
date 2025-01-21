import matplotlib.pyplot as plt
import numpy as np

# 数据
months = ["Dec", "Jan", "Feb", "Mar", "Apr", "May"]
cost = [260800, 378400, 203500, 277750, 197750, 44800]
cumulative_cost = np.cumsum(cost)  # 累积成本
print(sum(cost))

# 图形设置
fig, ax1 = plt.subplots()

# 绘制柱状图 (蓝色)
ax1.bar(months, cost, color="skyblue", label="Cost")
ax1.set_ylabel("Cost ($)", fontsize=12)
ax1.set_ylim(0, 400000)
ax1.tick_params(axis="y", labelsize=10)
ax1.legend(loc="upper left", fontsize=10)

# 添加第二个 y 轴
ax2 = ax1.twinx()
ax2.plot(months, cumulative_cost, color="orange", marker="o", label="Cumulative Cost", linewidth=2)
ax2.set_ylabel("Cumulative Cost ($)", fontsize=12, color="orange")
ax2.set_ylim(0, 1500000)
ax2.tick_params(axis="y", labelsize=10, colors="orange")
ax2.legend(loc="upper right", fontsize=10)

# 图标题和网格
plt.title("Cost and Cumulative Cost", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# 显示图形
plt.tight_layout()
plt.show()