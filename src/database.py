import json
from pyrsistent import s
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def format_db(dict_json):
    ans = []
    for key in dict_json:
        ans.append([key, dict_json[key]])
    return ans
    

def create_db_seq(data):
    i = 1
    seq_time = dict()
    for secuence in data:
        for event in secuence:
            if not event[0] in seq_time:
                seq_time[event[0]] = {}

            if not (i) in seq_time[event[0]]:
                seq_time[event[0]][(i)] = list()

            seq_time[event[0]][(i)].append([event[1][0], event[1][1]])
        i += 1
    format_db(seq_time)
    return seq_time


def create_df(data):
    sc = SparkSession.builder.getOrCreate()
    data_frame = [ ]
    i = 1
    for secuence in data:
        for event in secuence:
            data_frame.append((i, event[0], event[1][0], event[1][1]))
        i += 1
    
    columns = ['Sequence', 'Event', 'Start', 'End']

    df = sc.createDataFrame(data=data_frame, schema=columns)
    return df

def create_database(df_data):
    df_data = df_data.orderBy([ "Event", "Sequence", "Start", "End"],ascending = [ True, True,  True, True])
    df_collect = df_data.collect()
    db_created = []
    event_data = []
    element = ""
    for row in df_collect:
        if element != row["Event"]:
            element = row["Event"]
        
    return df_data
    pass

f = open('data.json')
data = json.load(f)
var = create_db_seq(data)
