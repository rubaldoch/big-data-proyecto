from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import time
from utils import *


class DHPG:
    def __init__(self, d_seq, n_seq, n_cores, support=0.6, confidence=0.6, verbose=False) -> None:
        """ Distributed Hierarchical Pattern Graph
        
        nodes = [   
            [],
            [level_1],
            [level_2],
            ...
        ]

        Args:
            d_seq (list): temporal sequence database
            n_seq (int): number of sequences 
            n_cores (int): number of cores to be used by spark
            support (float): support threshold
            confidence (float): confidence threshold
            verbose (bool): show all process to stdout

        """
        self.support = support
        self.confidence = confidence
        self.metricas = [(0,0) for i in range(3)] 
        self.nodes = [[]]
        conf = SparkConf()
        conf.setMaster("local[{}]".format(n_cores)).setAppName(
            "My app").set("spark.sql.shuffle.partitions", n_cores).set("spark.default.parallelism", n_cores)
        self.sc = SparkContext(conf=conf)
        self.spark = SparkSession(self.sc)
        self.d_ev = self.sc.parallelize(d_seq)
        self.verbose = verbose
        self.__preprocessing(n_seq)

    def __display_message(self, message):
        """ Print the given message to stdout.

        Args:
            message (str): message to display

        """
        n = 50
        m = (int) ((n - len(message) - 2)/2)
        print(n * "*")
        print("*" + (n-2) * " " + "*")
        print("*" + m * " " + message + m * " " + "*")        
        print("*" + (n-2) * " " + "*")
        print(n * "*")

    def __show_stats(self):
        """ Show execution statistics.
        
        """
        print("Preprocesamiento:")
        print("Exec Time:", round(self.metricas[0][0],2), "ms\t", "CPU Time:", round(self.metricas[0][1],2), "ms\n")
        print("Mine Single Freq Event:")
        print("Exec Time:", round(self.metricas[1][0],2), "ms\t", "CPU Time:", round(self.metricas[1][1],2), "ms\n")
        print("Mine Frequent 2-Event:")
        print("Exec Time:", round(self.metricas[2][0],2), "ms\t", "CPU Time:", round(self.metricas[2][1],2), "ms\n")

    def __preprocessing(self, n_seq):
        """ Converts the temporal sequence database 'd_seq' into an event database 'd_ev'
            and build the bitmap for each row in the event database.

        Args:
            n_seq (int): number of sequences

        """
        if self.verbose:
            self.__display_message("Preprocesamiento")
        ex_st = time.time()
        cpu_st = time.process_time()
        self.d_ev = self.d_ev.zipWithIndex()
        ex_et = time.time()
        cpu_et = time.process_time()
        exec_time = ex_et - ex_st
        cpu_time = cpu_et - cpu_st
        if self.verbose:
            print("temporal sequence database")
            self.d_ev.toDF().show()
        st = time.time()
        self.d_ev = self.d_ev.flatMap(
            lambda x: [(ev[0], x[1], ev[1]) for ev in x[0]]).toDF(["ev", "idx", "interval"])
        self.d_ev = self.d_ev.groupBy("ev", "idx").agg(
            F.collect_list(F.col("interval")).alias("interval"))
        self.d_ev = self.d_ev.rdd.groupBy(lambda x: x[0])
        self.d_ev = self.d_ev.map(
            lambda x: [x[0], {itr[1]:itr[2] for itr in list(x[1])}])
        self.d_ev = self.d_ev.map(lambda x: build_bitmap(x, n_seq))
        ex_et = time.time()
        cpu_et = time.process_time()
        exec_time += (ex_et - ex_st)
        cpu_time += (cpu_et - cpu_st)
        self.metricas[0] = (exec_time* 1000, cpu_time* 1000)
        if self.verbose:
            print("event database")
            self.d_ev.toDF().show()
            print("\n")
        


    def __mine_l1(self):
        """ Mining Frequent Single Events

        """
        ex_st = time.time()
        cpu_st = time.process_time()
        support = self.support
        level1 = self.d_ev.filter(lambda x: support_event(x) >= support)
        level1 = level1.map(lambda x: build_node1(x))
        self.nodes += [level1]
        ex_et = time.time()
        cpu_et = time.process_time()
        exec_time = ex_et - ex_st
        cpu_time = cpu_et - cpu_st
        self.metricas[1] = (exec_time* 1000, cpu_time* 1000)
        if self.verbose:
            self.__display_message("Mine 1-Freq ")
            print("event | bitmap | supp | conf")
            print("----------------------------")
            for el in level1.take(20):
                el.show()
            print("\n")
            

    def __mine_l2(self):
        """ Mining Frequent 2-Event Pattern

        """
        ex_st = time.time()
        cpu_st = time.process_time()
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
        ex_et = time.time()
        cpu_et = time.process_time()
        exec_time = ex_et - ex_st
        cpu_time = cpu_et - cpu_st
        self.metricas[2] = (exec_time* 1000, cpu_time* 1000)
        if self.verbose:
            self.__display_message("Mine 2-Freq ")
            print("event | bitmap | supp | conf")
            print("----------------------------")
            for el in level2.take(20):
                el.show()
            print("\n")

    def mine_pattern(self, show_stats=False):
        """ Mine frequent single and 2-event patterns

        Returns:
            Node: returns the level2 mining

        """
        
        self.__mine_l1()
        self.__mine_l2()
        if show_stats:
            self.__display_message("Estadísticas")
            self.__show_stats()
        return self.nodes[2]
    
