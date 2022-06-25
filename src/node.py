
class Node:
    def __init__(self, idx, bitmap, support, confidence):
        """ Node for the DHPG structure

        Args:
            idx (list): event(s) name index. Ej. 'A', 'AB', 'ABC', ...
            bitmap (int): bitmap value of the event
            support (int): support value
            confidence (int): confidence value

        """
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
