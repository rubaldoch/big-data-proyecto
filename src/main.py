from dhpg import DHPG
from generator import Generator


if __name__ == '__main__':
    gen = Generator(['A', 'B', 'C'], 1, 10, 3, True)
    d_seq = gen.generate()

    dphg = DHPG(d_seq, 5, 4)
    seq = dphg.mine_pattern().collect()
    [print(s.get_idx()) for s in seq]
