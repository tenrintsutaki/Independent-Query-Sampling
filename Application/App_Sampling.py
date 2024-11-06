from Tree_Sampling.Sampling import find_paths_and_collect, basic_sampling, basic_sampling_preprocess

def calculate_records_num(canonical_nodes):
    s = 0
    for node in canonical_nodes:
        s += node.weight
    return s
def sampling_application(root,values,left_idx,right_idx,k):
    canonical, weights = find_paths_and_collect(root,values[left_idx],values[right_idx]) # Find the canonical nodes
    total_records_num = calculate_records_num(canonical)
    basic_sampling_preprocess(canonical, weights)
    result = basic_sampling(canonical, k) # Sampled K Nodes as the result

