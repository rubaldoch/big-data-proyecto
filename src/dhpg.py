from pyspark import SparkContext 
from utils import *


class DHPG:
    def __init__(self, d_ev, n_seq, n_core, support=0.6, confidence=0.6) -> None:
        self.n_event = n_seq
        self.n_core = n_core
        self.support = support
        self.confidence = confidence
        self.sc = SparkContext(master="local[{}]".format(self.n_core)) 
        self.d_ev = self.sc.parallelize(d_ev)
        self.d_ev = self.d_ev.map(lambda x : build_bitmap(x, n_seq))
        self.nodes = [[]]

    def __mine_l1(self):
        support = self.support
        cur = self.d_ev.filter(lambda x : support_event(x) >= support)
        cur = cur.map(lambda x : build_node1(x))
        self.nodes += [cur]

    def __mine_l2(self):
        support = self.support
        confidence = self.support
        level1 = self.nodes[1]
        product = level1.cartesian(level1).map(lambda x: build_nodek(x[0], x[1]))
        product = product.filter(lambda x : x.get_idx() == sorted(x.get_idx()))
        level2 = product.filter(lambda x : 
                                    x.get_support() >= support 
                                    and x.get_confidence() >= confidence)
        self.nodes += [level2]

    def mine_pattern(self):
        self.__mine_l1()
        self.__mine_l2()
        return self.nodes[2].collect()

