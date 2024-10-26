import pandas as pd
import numpy as np


def generate(num):
    id = np.linspace(1,num,num,dtype=int)
    print(id)
    np.random.seed(42)
    age = np.random.randint(18, 66, size=num)  # 生成100个年龄数据，范围在18到65
    slope = 3000  # 线性斜率
    intercept = 20000  # 截距
    income = intercept + slope * (age - 18) + np.random.normal(0, 10000, size=age.shape)
    # 创建 DataFrame
    data = pd.DataFrame({
        'ID': id,
        'Age': age,
        'Income': income
    })
    # 将数据写入 CSV 文件
    data.to_csv('data/data.csv', index=False)
    print("Data has been generated and written to data.csv.")


if __name__ == "__main__":
    generate(100000)