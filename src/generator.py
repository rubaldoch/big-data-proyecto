from faker import Faker
import random

from torch import rand

facker = Faker()

def create_event(event_name, nr_events):
    events = []
    dates = []
    for i in range(nr_events*2):
        dates.append(facker.date_time_between(start_date='-60d', end_date='now'))
    dates.sort()
    for i in range(nr_events):
        events.append((event_name, [dates[i*2],dates[i*2+1]]))
    return events;

def create_multiple_events(list_name, min_events, max_events):
    all_events = []
    for name in list_name:
        number_events = random.randint(min_events, max_events)
        events = create_event(name, number_events)
        for event in events:
            all_events.append(event)
    random.shuffle(all_events)
    return all_events


