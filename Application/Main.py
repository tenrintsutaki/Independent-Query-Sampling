import pandas as pd

from Application.Create_Data import generate, preprocess, weight_compute
from Tree_Sampling.Construction_Tools import construct_bst, build_AS_structure, construct_bst_with_element
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes
from Application.App_Sampling import sampling_application

if __name__ == '__main__':
    left_val = 20
    right_val = 35
    k = 500
    generate(100000,'data/data.csv')
    df = pd.read_csv('data/data.csv')
    unique,values,grouped_id = preprocess('data/data.csv','Age')
    # group_id: {Age:[id1,id2,id3]}
    unique.sort()
    ls = []
    for u in unique:
        ls.append(u)

    weight_dict = sorted(weight_compute(values).items(),key = lambda x:x[0])
    elements = [item[0] for item in weight_dict]
    root,leaf_index = construct_bst_with_element(ls, elements, grouped_id)
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root)

    # APPLICATION PART#
    temp,total_num = sampling_application(root,left_val,right_val,k,df)

    for node in temp:
        print(node)
        print(node.weight)
        print(node.ptrs)
        print("\n")
