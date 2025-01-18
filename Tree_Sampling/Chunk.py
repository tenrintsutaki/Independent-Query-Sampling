
class Chunk():
    def __init__(self, l, r, length):
        self.l = l
        self.r = r
        self.length = length
    # Alias抽取的内容转换为chunk，内存开销 -> 1/logN
    # Mapping relationship: a data mapped by a chunk (1 to many)