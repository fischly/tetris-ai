import numpy as np

class PieceData():
    def __init__(self, piece_id, data, num_rot, start_x_position):
        self.num_rot = num_rot
        self.start_x_position = start_x_position
        self.piece_id = piece_id
        
        self.data = data
        
        self.margins = []
        for rot in range(num_rot):
            npdata = np.array(data[rot])
            
            left = npdata[:, 1].min()
            right = npdata[:, 1].max()
        
            self.margins.append((left, right))
    
    def __str__(self):
        return '\n'.join(map(lambda x: str(x), self.data))
    
    def __repr__(self):
        return self.__str__()
        
        
piece_data = []

# 0: t-piece
piece_data.append(PieceData(0, [((0, 1), (1, 0), (1, 1), (1, 2)),((0, 1), (1, 1), (1, 2), (2, 1)),((1, 0), (1, 1), (1, 2), (2, 1)),((0, 1), (1, 0), (1, 1), (2, 1))], 4, 3))
# 1: l-piece
piece_data.append(PieceData(1, [((0, 2), (1, 0), (1, 1), (1, 2)),((0, 1), (1, 1), (2, 1), (2, 2)),((1, 0), (1, 1), (1, 2), (2, 0)),((0, 0), (0, 1), (1, 1), (2, 1))], 4, 3))
# 2: j-piece
piece_data.append(PieceData(2, [((0, 0), (1, 0), (1, 1), (1, 2)),((0, 1), (0, 2), (1, 1), (2, 1)),((1, 0), (1, 1), (1, 2), (2, 2)),((0, 1), (1, 1), (2, 0), (2, 1))], 4, 3))
# 3: o-piece
piece_data.append(PieceData(3, [((0, 1), (0, 2), (1, 1), (1, 2)),((0, 1), (0, 2), (1, 1), (1, 2)),((0, 1), (0, 2), (1, 1), (1, 2)),((0, 1), (0, 2), (1, 1),(1, 2))], 1, 4))
# 4: i-piece
piece_data.append(PieceData(4, [((1, 0), (1, 1), (1, 2), (1, 3)), ((0, 2), (1, 2), (2, 2), (3, 2)), ((2, 0), (2, 1), (2, 2), (2, 3)),((0, 1), (1, 1), (2, 1), (3, 1))], 4, 3))
# 5: s-piece
piece_data.append(PieceData(5, [((0, 1), (0, 2), (1, 0), (1, 1)),((0, 1), (1, 1), (1, 2), (2, 2)),((1, 1), (1, 2), (2, 0), (2, 1)),((0, 0), (1, 0), (1, 1), (2, 1))], 4, 3))
# 6: z-piece
piece_data.append(PieceData(6, [((0, 0), (0, 1), (1, 1), (1, 2)),((0, 2), (1, 1), (1, 2), (2, 1)),((1, 0), (1, 1), (2, 1), (2, 2)),((0, 1), (1, 0), (1, 1), (2, 0)),], 4, 3))


kicks = {
    # (kick_from, kick_to): (offset1, offset2, offset3, offset4)
    (0, 1): ((+0, -1), (-1, -1), (+2, +0), (+2, -1)),  # 0 -> R | CW
    (0, 3): ((+0, +1), (-1, +1), (+2, +0), (+2, +1)),  # 0 -> L | CCW
    (1, 0): ((+0, +1), (+1, +1), (-2, +0), (-2, +1)),  # R -> 0 | CCW
    (1, 2): ((+0, +1), (+1, +1), (-2, +0), (-2, +1)),  # R -> 2 | CW
    (2, 1): ((+0, -1), (-1, -1), (+2, +0), (+2, -1)),  # 2 -> R | CCW
    (2, 3): ((+0, +1), (-1, +1), (+2, +0), (+2, +1)),  # 2 -> L | CW
    (3, 0): ((+0, -1), (+1, -1), (-2, +0), (-2, -1)),  # L -> 0 | CW
    (3, 2): ((+0, -1), (+1, -1), (-2, +0), (-2, -1)),  # L -> 2 | CCW
}

i_kicks = {
    (0, 1): ((+0, -2), (+0, +1), (+1, -2), (-2, +1)),  # 0 -> R | CW
    (0, 3): ((+0, -1), (+0, +2), (-2, -1), (+1, +2)),  # 0 -> L | CCW
    (1, 0): ((+0, +2), (+0, -1), (-1, +2), (+2, -1)),  # R -> 0 | CCW
    (1, 2): ((+0, -1), (+0, +2), (-2, -1), (+1, +2)),  # R -> 2 | CW
    (2, 1): ((+0, +1), (+0, -2), (+2, +1), (-1, +2)),  # 2 -> R | CCW
    (2, 3): ((+0, +2), (+0, -1), (-1, +2), (+2, -1)),  # 2 -> L | CW
    (3, 0): ((+0, +1), (+0, -2), (+2, +1), (-1, -2)),  # L -> 0 | CW
    (3, 2): ((+0, -2), (+0, +1), (+1, -2), (-2, +1)),  # L -> 2 | CCW
}