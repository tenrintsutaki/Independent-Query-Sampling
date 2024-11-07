import pandas as pd

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
    query_rate,total_number = sampling_application(root,left_val,right_val,k,df,query)
    print("------ Sampling Result ------")
    print(f"Rate of this query in sampling is:",query_rate)
    print(f"Estimated there are {int(query_rate * total_number)} records in {total_number} satisfied this condition.")

