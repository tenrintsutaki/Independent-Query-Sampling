<<<<<<< HEAD
# Independent-Query-Sampling
IQS project for CMSC5720/CMSC5721
=======
### Progress in IQS Project (Term 1)

## Week 1

### Done:
- Read the paper from Section 1 to Section 4.1
- Implement / Test the Alias structure in Python
- Try to combine the BST with AS

### Plan:
- Implement the basic Tree Sampling algorithm
- Visualization of the Sampling (Not sure)
- Read

### Questions:
1. In section 3.2
   1. "For a node 𝑞 of 𝑇 , a weighted sample from the subtree of
𝑞 is a random variable 𝑋 such that Pr[𝑋 = 𝑧] = 𝑤(𝑧)/𝑤(𝑞). for each leaf 𝑧 in the subtree.", and "If 𝑞 is a leaf, return it directly.", 
Could the first "q" is a leaf ? If so, the w(z) == w(q) ?

   2. "See Figure 1 for an illustration. To draw a weighted sample of
𝑆𝑞, we first sample a node 𝑋 from C", how to sample a node from C? Because the node in C is **disjoint**, I think it could not be sampled by using AS.


2. In section 4.1
   1. In section 3.2, "Each time we could sample a children node from q", but in 4.1 seems like the node could only sample leaves, not children nodes.


## Week 3

### Done: 
- Finish the initial version of "Finding canonical nodes in efficient way"
- Finish the search function of the BST (update val of each node)
- Do the basic experiment of sampling

### Problems:
- "Edge cases" for the checking canonical nodes
- Verify the method of sampling experiment.
>>>>>>> master
