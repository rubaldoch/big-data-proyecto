from faker import Faker
import random
import json
import datetime

facker = Faker()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)

def create_event(event_name, nr_events):
    events = []
    dates = []
    for i in range(nr_events*2):
        dates.append(facker.date_time_between(start_date='-60d', end_date='now'))
    dates.sort()
    for i in range(nr_events):
        events.append((event_name, [dates[i*2],dates[i*2+1]]))
    return events;

def create_sequence(list_name, min_events, max_events):
    sequence = []
    for name in list_name:
        number_events = random.randint(min_events, max_events)
        events = create_event(name, number_events)
        for event in events:
            sequence.append(event)
    random.shuffle(sequence)
    return sequence


def create_multiple_sequences(list_name, min_events, max_events, nr_sequences, write=False):
    all_sequences = []
    for i in range(nr_sequences):
        all_sequences.append(create_sequence(list_name, min_events, max_events))
    if write:
        with open("data.json", "w") as i :
            json.dump(all_sequences, i, cls=DateTimeEncoder)
    return all_sequences
#Usage create_multiple_sequences(['A', 'B', 'C'], 1, 10, 3, True)
