
from Tree_Sampling.Sampling import find_paths_and_collect, basic_sampling, basic_sampling_preprocess
from Tree_Sampling.Sampling_Alias import alias_sampling, leaf_sampling_alias, leaf_sampling_alias_application
import random

def calculate_records_num(canonical_nodes):
    s = 0
    for node in canonical_nodes:
        s += node.weight
    return s

def sampling_application(root,left_val,right_val,k,df,query):
    canonical, weights = find_paths_and_collect(root,left_val,right_val) # Find the canonical nodes
    total_records_num = calculate_records_num(canonical)
    basic_sampling_preprocess(canonical, weights)
    result = alias_sampling(canonical, k) # Sample a canonical node firstly from AS Sampling*
    leaves = []
    values = []
    for node in result:
        res = leaf_sampling_alias_application(node) # Then use alias sampling to get the result
        leaves.append(res)
    correct = 0
    for leaf in leaves: # leaf is a leaf node
        id = random.choice(leaf.ptrs)
        record = df[df["ID"] == id]
        if(check_rule(query,record)):
            correct += 1
            values.append(1)
        else:
            values.append(0)
    return (correct / k),total_records_num,values

def check_rule(query,row):
    row_dict = row.to_dict('records')[0] # 神奇代码 完全看不懂但是管用
    # 使用 eval 函数来评估查询条件
    return eval(query, {}, row_dict)