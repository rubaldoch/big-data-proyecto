from node import Node
import numpy as np


def build_bitmap(x, n_seq):
    """ Build a n_seq bitmap to an x event instance on event database
    
    x = [event_name, {
        idx_1:[[time_start, end_time], ... ],
        idx_2:[[time_start, end_time], ... ], 
        ...}]

    Args:
        x (list): event database instance
        n_seq (int): number of sequences

    Returns:
        list: [event database instance, bitmap]

    """
    bitmap = [0 for _ in range(n_seq)]
    for key in x[1].keys():
        bitmap[key] = 1
    return x + [bitmap]


def get_support(bitmap):
    """ Return a support value to a given bitmap
    
    Args:
        bitmap(list): an event bitmap 
    
    Returns:
        float: support value

    """
    return sum(bitmap)/len(bitmap)


def support_event(x):
    """ Return a suppor tvalue of x event instance on event database (d_ev)
    
    Args:
        x (list): event database instance

    Returns:
        float: support value of event instance

    """
    return get_support(x[2])


def confidence_event(x, y):
    pass


def build_node1(x):
    """ Build a node for the single event instance
    
    Args:
        x (list): event database instance
    
    Returns:
        Node: a node for the single event instance

    """
    support = support_event(x)
    confidence = 1
    return Node([x[0]], np.array(x[2]), support, confidence)


def build_nodek(x, y):
    """ Build a node for k-frequent event pairs
    
    Args:
        x (Node): node of k-1 level
        y (Node): node of k-1 level
    
    Returns:
        Node: a node for k-frequent x and y event pairs

    """
    idx = x.get_idx() + y.get_idx()
    bitmap = x.get_bitmap() & y.get_bitmap()
    support = get_support(bitmap)
    confidence = support / max(x.get_support(), y.get_support())
    return Node(idx, bitmap, support, confidence)
