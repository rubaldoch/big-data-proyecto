import json

from dhpg import DHPG
from database import create_db_seq
from generator import create_multiple_sequences


d_ev = [
    ["A", {
        0: [
            [1.0, 2.0],
            [9.0, 11.0]
        ],
        1: [
            [6.0, 7.0]
        ],
        2: [
            [10.0, 12.0]
        ],
        3: [
            [10.0, 12.0],
            [18.3, 19.0]
        ],
        4: [
            [7.0, 8.0]
        ]
    }],
    ["B", {
        0: [
            [2.3, 5.0]
        ],
        1: [
            [8.0, 10.0],
            [22.0, 23.0]
        ],
        2: [
            [12.3, 15.0]
        ],
        3: [
            [12.0, 15.0]
        ],
        4: [
            [8.0, 12.0]
        ]
    }],
    ["C", {
        0: [
            [4.0, 5.0]
        ],
        1: [
            [6.0, 7.3],
            [9.0, 10.0]
        ],
        2: [
            [13.0, 14.3]
        ],
        3: [
            [13.0, 14.0]
        ],
        4: [
            [10.0, 12.0]
        ]
    }],
    ["D", {
        0: [
            [4.3, 6.0]
        ],
        1: [
            [9.3, 11.0]
        ],
        2: [
            [1.0, 4.0],
            [14.0, 17.0]
        ],
        3: [
            [13.3, 16.0]
        ],
        4: [
            [11.0, 16.0]
        ]
    }],
    ["E", {
        0: [
            [0.3, 1.0]
        ],
        2: [
            [19.0, 21.0]
        ],
        4: [
            [18.0, 21.0]
        ]
    }],
    ["F", {
        3: [
            [13.0, 21.0]
        ]
    }]
]

# Usage create_multiple_sequences(['A', 'B', 'C'], 1, 10, 3, True)
create_multiple_sequences(['A', 'B', 'C'], 1, 10, 3, True)

f = open('data.json')
data = json.load(f)
var = create_db_seq(data)

dphg = DHPG(d_ev, 5, 4)
seq = dphg.mine_pattern()
[print(s.get_idx()) for s in seq]
