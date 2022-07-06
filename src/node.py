
class Node:
    def __init__(self, idx, bitmap, support, confidence):
        """ Node for the DHPG structure

        Args:
            idx (list): event(s) name index. Ej. 'A', 'AB', 'ABC', ...
            bitmap (array): bitmap value of the event
            support (float): support value
            confidence (float): confidence value

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

    def show(self):
        print(self.idx,"|",self.bitmap,"|",self.support,"|",self.confidence)