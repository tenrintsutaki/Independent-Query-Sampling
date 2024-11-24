import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from Application.Create_Data import generate, preprocess, weight_compute
from Tree_Sampling.Construction_Tools import construct_bst, build_AS_structure, construct_bst_with_element
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from Application.App_Sampling import sampling_application

def generate():
    generate(100000,'data/data.csv')

if __name__ == '__main__':
    left_val = 20
    right_val = 35
    k = 5000
    # generate(100000,'data/data.csv')
    df = pd.read_csv('data/data.csv')
    unique,values,grouped_id = preprocess('data/data.csv','Age')
    # group_id: {Age:[id1,id2,id3]}
    unique.sort()
    ls = []
    for u in unique:
        ls.append(u)

    weight_dict = sorted(weight_compute(values).items(),key = lambda x:x[0])
    elements = [item[1] for item in weight_dict]
    root,leaf_index = construct_bst_with_element(ls, elements, grouped_id)
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root)

    # APPLICATION PART#
    query = "Gender == 0 and Married == 0"
    query_rate,total_number,values = sampling_application(root,left_val,right_val,k,df,query)
    print("------ Sampling Result ------")
    print(f"Rate of this query in sampling is:",query_rate)
    print(f"Estimated there are {int(query_rate * total_number)} records in {total_number} satisfied this condition.")

    total_num_list = []
    total_num_list_upper = []
    total_num_list_lower = []
    k_list = []
    for k in range(10,2000,50):
        estimate,total_number,values = sampling_application(root, left_val, right_val, k, df, query)
        total_num_list.append(np.mean(values))
        k_list.append(k)
    for val in total_num_list:
        total_num_list_upper.append(val + (np.std(val) * 1.96) / np.sqrt(len(total_num_list)))
        total_num_list_lower.append(val - (np.std(val) * 1.96) / np.sqrt(len(total_num_list)))
    # x_values = []
    # y_values = []
    #
    # for i, yi in enumerate(total_num_list):
    #     # 对于 y 中的每个子列表 yi，复制 x[i] 并与 yi 中的每个值配对
    #     x_values.extend([k_list[i]] * len(yi))
    #     y_values.extend(yi)

    plt.figure(figsize=(5, 5))
    plt.plot(k_list, total_num_list)
    plt.plot(k_list, total_num_list_upper)
    plt.plot(k_list, total_num_list_lower)
    plt.ylabel('Variance')
    # ax2.plot(selectivity_vals, time_vals_canonical, label='Canonical')
    plt.xlabel('K')
    plt.legend()
    # plt.title(f'Nodes: {num_nodes}, Memory Cost: {memory_info.rss / (1024 * 1024 * 1024):.2f} GB, S = {k}')
    plt.show()
