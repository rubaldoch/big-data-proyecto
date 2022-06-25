from dhpg import DHPG
from generator import TSD


if __name__ == '__main__':
    # Generate temporal event sequence
    tsd = TSD(['A', 'B', 'C'], 1, 10, 3, True)
    d_seq = tsd.generate()

    # Mining 2-Frequent events
    dphg = DHPG(d_seq, 3, 4)
    seq = dphg.mine_pattern().collect()
    [print(s.get_idx()) for s in seq]
