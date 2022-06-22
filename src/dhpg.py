from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from utils import *


class DHPG:
    def __init__(self, d_seq, n_seq, n_core, support=0.6, confidence=0.6) -> None:
        self.support = support
        self.confidence = confidence
        self.nodes = [[]]
        conf = SparkConf()
        conf.setMaster("local[{}]".format(n_core)).setAppName(
            "My app").set("spark.sql.shuffle.partitions", n_core).set("spark.default.parallelism", n_core)
        self.sc = SparkContext(conf=conf)
        self.spark = SparkSession(self.sc)
        self.d_ev = self.sc.parallelize(d_seq)
        self.__build_dev(n_seq)

    def __build_dev(self, n_seq):
        self.d_ev = self.d_ev.zipWithIndex()
        self.d_ev = self.d_ev.flatMap(
            lambda x: [(ev[0], x[1], ev[1]) for ev in x[0]]).toDF(["ev", "idx", "interval"])
        self.d_ev = self.d_ev.groupBy("ev", "idx").agg(
            F.collect_list(F.col("interval")).alias("interval"))
        self.d_ev = self.d_ev.rdd.groupBy(lambda x: x[0])
        self.d_ev = self.d_ev.map(
            lambda x: [x[0], {itr[1]:itr[2] for itr in list(x[1])}])
        self.d_ev = self.d_ev.map(lambda x: build_bitmap(x, n_seq))

    def __mine_l1(self):
        support = self.support
        level1 = self.d_ev.filter(lambda x: support_event(x) >= support)
        level1 = level1.map(lambda x: build_node1(x))
        self.nodes += [level1]

    def __mine_l2(self):
        support = self.support
        confidence = self.support
        level1 = self.nodes[1]
        product = level1.cartesian(level1).map(
            lambda x: build_nodek(x[0], x[1]))
        product = product.filter(lambda x: x.get_idx() == sorted(x.get_idx()))
        level2 = product.filter(lambda x:
                                x.get_support() >= support
                                and x.get_confidence() >= confidence)
        self.nodes += [level2]

    def mine_pattern(self):
        self.__mine_l1()
        self.__mine_l2()
        return self.nodes[2]
