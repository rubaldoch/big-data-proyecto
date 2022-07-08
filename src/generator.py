import random
import json
import datetime
from faker import Faker

faker = Faker()
class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


class TSD:
    def __init__(self, event_names_list, min_event_ocurr, max_event_ocurr, number_of_sequences, write_to_file=False):
        """Temporal Sequence Database

        Args
            event_names_list (list): list of event names
            min_event_ocurr (int): min ocurrences of each event
            max_event_ocurr (int): max ocurrences of each event
            number_of_sequences (int): number of temporal sequences
            write_to_file (bool): save TDS to data.json file

        """
        self.event_names_list = event_names_list if not(event_names_list) or len(event_names_list) else faker.words(26)
        self.min_event_ocurr = min_event_ocurr
        self.max_event_ocurr = max_event_ocurr
        self.number_of_sequences = number_of_sequences
        self.write_to_file = write_to_file


    def __create_temporal_events(self, event_name, num_event_ocurr):
        """Creates an list of temporal event ocurrences
        [
            (event_name, [start_time_1, end_time_1]), 
            (event_name, [start_time_2, end_time_2]),
            ...
        ]

        Args
            event_name (str): Event name
            num_event_ocurr (int): Number of event ocurrences  

        Returns:
            list: a temporal event list

        """

        events = []
        times = []
        for i in range(num_event_ocurr*2):
            times.append(round(random.uniform(0.0, 300.0), 2))
        times.sort()
        for i in range(num_event_ocurr):
            events.append((event_name, [times[i*2], times[i*2+1]]))
        return events


    def __create_temporal_sequence(self, event_names_list, min_event_ocurr, max_event_ocurr):
        """Creates a sequence of event instances chronologically ordered by their start time
        [
            (event_7, [start_time_1, end_time_1]),
            (event_2, [start_time_2, end_time_2]),
            (event_4, [start_time_3, end_time_3]),
            ...
        ]

        Args
            event_names_list (list): list of event names
            min_event_ocurr (int): min ocurrences of each event
            max_event_ocurr (int): max ocurrences of each event

        Returns:
            list: temporal event sequence

        """
        sequence = []
        for name in event_names_list:
            number_events = random.randint(min_event_ocurr, max_event_ocurr)
            events = self.__create_temporal_events(name, number_events)
            for event in events:
                sequence.append(event)
        sequence.sort(key=lambda x:x[1][0])
        return sequence


    def generate(self):
        """Generate a temporal sequence database (Dseq). 
        A Dseq is a collection of temporal sequences
        [
            [(ev_7, [start_time, end_time]), ...],
            [(ev_3, [start_time, end_time]), ...],
            [(ev_1, [start_time, end_time]), ...],
            ...      
        ]

        Returns:
            list: a list of temporal sequences

        """
        database = []
        for i in range(self.number_of_sequences):
            database.append(self.__create_temporal_sequence(
                self.event_names_list, self.min_event_ocurr, self.max_event_ocurr))
        if self.write_to_file:
            with open("data.json", "w") as i:
                json.dump(database, i, cls=DateTimeEncoder)
        return database
