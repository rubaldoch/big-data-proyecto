import string
from dhpg import DHPG
from generator import TSD


if __name__ == '__main__':
    # Generate temporal event sequence
    alphabet_string = list(string.ascii_uppercase)
    tsd = TSD(alphabet_string, 50, 100, 20)
    d_seq = tsd.generate()

    # Mining 2-Frequent events
    dphg = DHPG(d_seq, 20, 4, verbose=True)
    seq = dphg.mine_pattern(True)
