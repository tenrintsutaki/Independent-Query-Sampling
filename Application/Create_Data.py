import collections
import pandas as pd
import numpy as np
from Tree_Sampling.Construction_Tools import construct_bst, build_AS_structure, construct_bst_with_element
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes

def generate(num,path):
    id = np.linspace(1,num,num,dtype=int)
    np.random.seed(114514)
    age = np.random.randint(18, 66, size=num) # 生成100个年龄数据，范围在18到65
    gender = np.random.randint(0,2, size=num)
    # married = np.random.randint(0,2, size=num)
    probabilities = [0.5,0.5]
    married = np.random.choice([0, 1], size=num, p=probabilities)
    slope = 3000  # 线性斜率
    intercept = 20000  # 截距
    income = intercept + slope * (age - 18) + np.random.normal(0, 10000, size=age.shape)
    # 创建 DataFrame
    data = pd.DataFrame({
        'ID': id,
        'Age': age,
        'Income': income,
        'Gender' : gender,
        'Married': married,
    })
    # 将数据写入 CSV 文件
    data.to_csv(path,index=False)
    print("Data has been generated and written to data.csv.")

def preprocess(path,feature):
    data = pd.read_csv(path)
    num_list = data[feature]
    grouped = data.groupby(feature)['ID'].apply(list).to_dict()
    return num_list.unique(),num_list.values,grouped

def weight_compute(input_data):
    d = collections.defaultdict(int)
    for data in input_data:
        d[data] += 1
    return d

if __name__ == "__main__":
    generate(100000,'data/data.csv')
    unique,values,grouped_id = preprocess('data/data.csv','Age')
    # group_id: {Age:[id1,id2,id3]}
    # unique.sort()
    # ls = []
    # for u in unique:
    #     ls.append(u)
    # weight_dict = sorted(weight_compute(values).items(),key = lambda x:x[0])
    # elements = [item[0] for item in weight_dict]
    # root,leaf_index = construct_bst_with_element(ls, elements, grouped_id)
    # calculate_weight(root)
    # update_internal_nodes(root)
    # build_AS_structure(root)
