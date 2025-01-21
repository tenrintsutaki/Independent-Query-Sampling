
class Chunk_Structure():
    def __init__(self, raw, weight):
        self.r = None
        self.l = None
        self.AS = None
        self.raw = raw
        self.weight = weight
    # Alias抽取的内容转换为chunk，内存开销 -> 1/logN
    # Mapping relationship: a data mapped by a chunk (1 to many)
    def initialize(self):
        self.l = self.raw[0]
        self.r = self.raw[-1]
        