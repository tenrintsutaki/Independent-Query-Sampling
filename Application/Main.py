from Application.Create_Data import generate, preprocess

if __name__ == '__main__':
    generate(100000,'data/data.csv')
    values = preprocess('data/data.csv','Age')
    root, leaf_index = construct_bst(values, weights, 0)
    calculate_weight(root)
    update_internal_nodes(root)
    # update_intervals(root)
    # build_AS_structure_direct_node(root)
    build_AS_structure(root)