import sys
import string
from dhpg import DHPG
from generator import TSD


if __name__ == '__main__':
    # Generate temporal event sequence
    alphabet_string = list(string.ascii_uppercase)
    n = int(sys.argv[1]) if (len(sys.argv) > 1) else 100
    tsd = TSD(alphabet_string, 50, 100, n)
    d_seq = tsd.generate()

    # Mining 2-Frequent events
    dphg = DHPG(d_seq, n, 4, verbose=True)
    seq = dphg.mine_pattern(True)
