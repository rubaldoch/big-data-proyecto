from node import Node
import numpy as np


def build_bitmap(x, n_seq):
    bitmap = [0 for _ in range(n_seq)]
    for key in x[1].keys():
        bitmap[key] = 1
    return x + [bitmap]

def get_support(bitmap):
    return sum(bitmap)/len(bitmap)

def support_event(x):
    return get_support(x[2])

def confidence_event(x, y):
    pass

def build_node1(x):
    support = support_event(x)
    condidence = 1
    return Node([x[0]], np.array(x[2]), support, condidence)

def build_nodek(x, y):
    idx = x.get_idx() + y.get_idx()
    bitmap = x.get_bitmap() & y.get_bitmap()
    support = get_support(bitmap)
    confidence = support / max(x.get_support(), y.get_support())
    return Node(idx, bitmap, support, confidence)