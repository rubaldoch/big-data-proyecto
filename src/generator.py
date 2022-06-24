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


class Generator:

    def __init__(self, names_list, min_event_ocurr, max_event_ocurr, num_rand_seq, write_to_file=False):
        """Generate multiple event sequences

        Args
            names_list (list): List of event names
            min_event_ocurr (int): min ocurrences of each event
            max_event_ocurr (int): max ocurrences of each event

        Returns:
            list: a list of events

        """
        self.names_list = names_list
        self.min_event_ocurr = min_event_ocurr
        self.max_event_ocurr = max_event_ocurr
        self.num_rand_seq = num_rand_seq
        self.write_to_file = write_to_file


    def __create_event_ocurr(self, event_name, n_rand_ocurr):
        """Creates an list of ocurrences of an event

        Args
            event_name (str): Event name
            n_rand_ocurr (int): Number of ramdom ocurrences of the event

        Returns:
            list: a list of tuples of ocurrence events [(event_name, [ocurr_initial, ocurr_final])]

        """

        events = []
        ocurrences = []
        for i in range(n_rand_ocurr*2):
            ocurrences.append(round(random.uniform(0.0, 300.0), 2))
        ocurrences.sort()
        for i in range(n_rand_ocurr):
            events.append((event_name, [ocurrences[i*2], ocurrences[i*2+1]]))
        return events


    def __create_events_ocurr_sequence(self, names_list, min_event_ocurr, max_event_ocurr):
        """Creates a sequence of events ocurrences given a name's list

        Args
            names_list (list): List of event names
            min_event_ocurr (int): min ocurrences of each event
            max_event_ocurr (int): max ocurrences of each event

        Returns:
            list: a list of events

        """
        sequence = []
        for name in names_list:
            number_events = random.randint(min_event_ocurr, max_event_ocurr)
            events = self.__create_event_ocurr(name, number_events)
            for event in events:
                sequence.append(event)
        return sequence


    def generate(self):
        """Generate multiple event sequences

        Returns:
            list: a list of events

        """
        all_sequences = []
        for i in range(self.num_rand_seq):
            all_sequences.append(self.__create_events_ocurr_sequence(
                self.names_list, self.min_event_ocurr, self.max_event_ocurr))
        if self.write_to_file:
            with open("data.json", "w") as i:
                json.dump(all_sequences, i, cls=DateTimeEncoder)
        return all_sequences
