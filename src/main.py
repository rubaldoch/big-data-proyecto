from dhpg import DHPG
from generator import TSD


if __name__ == '__main__':
    tsd = TSD(['A', 'B', 'C'], 1, 10, 3, True)
    d_seq = tsd.generate()

    dphg = DHPG(d_seq, 5, 4)
    seq = dphg.mine_pattern().collect()
    [print(s.get_idx()) for s in seq]
