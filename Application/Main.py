from Application.Create_Data import generate, preprocess, weight_compute
from Tree_Sampling.Construction_Tools import construct_bst, build_AS_structure
from Tree_Sampling.Sample_Tools import calculate_weight, update_internal_nodes

if __name__ == '__main__':
    generate(100000,'data/data.csv')
    unique,values = preprocess('data/data.csv','Age')
    unique.sort()
    ls = []
    for u in unique:
        ls.append(u)
    weight_dict = sorted(weight_compute(values).items(),key = lambda x:x[0])
    elements = [item[1] for item in weight_dict]
    root,leaf_index = construct_bst(ls, elements, 0)
    calculate_weight(root)
    update_internal_nodes(root)
    build_AS_structure(root)