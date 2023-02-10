from tetris.PieceData import piece_data

class Piece():
    def __init__(self, ptype, pos=None, rot=0):
        self.pos = pos if pos is not None else [0, piece_data[ptype].start_x_position]
        self.rot = rot
        self.ptype = ptype
        self.pdata = piece_data[ptype]
    
    def __str__(self):
        return str(self.pdata)
    def __repr__(self):
        return self.__str__()
    
    def clone(self, ptype=None, pos=None):
        if ptype is None:
            ptype = self.ptype
        if pos is None:
            pos = self.pos
        
        return Piece(ptype, pos)