
class TreeNode():
    def __init__(self,left = None,right = None,val = None,weight = 0,ptrs = None):
        self.left = left
        self.right = right
        self.weight = weight
        # self.sample_weight = 0 # Memory
        self.val = val
        self.AS = None
        # self.interval = None
        self.ptrs = ptrs

    def is_leaf(self):
        return self.left is None and self.right is None
