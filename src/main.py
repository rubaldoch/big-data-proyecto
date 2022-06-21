import json

from dhpg import DHPG
from generator import create_multiple_sequences

# Usage create_multiple_sequences(['A', 'B', 'C'], 1, 10, 3, True)
create_multiple_sequences(['A', 'B', 'C'], 1, 10, 3, True)

f = open('data.json')
d_seq = json.load(f)

dphg = DHPG(d_seq, 5, 4)
seq = dphg.mine_pattern().collect()
[print(s.get_idx()) for s in seq]
