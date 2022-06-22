
class Node:
    def __init__(self, idx, bitmap, support, confidence):
        self.idx = idx
        self.bitmap = bitmap
        self.support = support
        self.confidence = confidence

    def get_idx(self):
        return self.idx

    def get_bitmap(self):
        return self.bitmap

    def get_support(self):
        return self.support

    def get_confidence(self):
        return self.confidence
