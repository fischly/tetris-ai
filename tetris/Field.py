import numpy as np

from tetris.PieceData import PieceData, kicks, i_kicks
from tetris.Piece import Piece

class Field():
    def __init__(self, shape=(20, 10), data=None):
        if data is None:
            self.field_data = np.zeros(shape)
        else:
            self.field_data = data

        self.width = shape[1]
        self.height = shape[0]
        
        
    def _extract_piece_info(self, piece, rot, pos=None):
        px = piece.pos[0] if pos is None else pos[0]
        py = piece.pos[1] if pos is None else pos[1]
        
        return (px, py)
    
        
    def is_collision(self, piece, rot, pos=None):
        """ Returns whether the given piece collides with the current field. """
        # check if collision between shape and existing play field
        # if 'pos' is not passed, it will use the piece's position
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        for x, y in piece.pdata.data[rot]:
            if x + px not in range(self.field_data.shape[0]):
                return True

            if y + py not in range(self.field_data.shape[1]):
                return True

            if self.field_data[x + px, y + py] != 0:
                return True

        return False
    
    def handle_clears(self, state, piece, rot, pos=None):
        """Finds completed lines, removes them and returns the score achieved by this piece placement, or None if its gameover."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        # state = self._add_piece_to_board(piece, rot, pos)
        
        # check for gameover
        if any(state[0]):
            return None
        
        # check for t-spin
        is_tspin = False
        if piece.ptype == 0: # if T-piece
            if self.is_collision(piece, rot, [px - 1, py]) and self.is_collision(piece, rot, [px, py + 1]) and self.is_collision(piece, rot, [px, py - 1]):
                is_tspin = True
        
        # check for cleared rows, and remove them
        cleared_rows = 0
        for idx, row in enumerate(state):
            if np.all(row):
                cleared_rows += 1
                
                state[1 : idx + 1] = state[:idx]
                state[0] = [0] * 10
        
        # check if a all-clear was done
        is_all_clear = all(
            all(c == 0 for c in row)
            for row in state
        )
        
        # print(f'cleared_lines: {cleared_rows}, is_tspin: {is_tspin}, is_all_clear: {is_all_clear}, combo={self.current_combo}, btb={self.current_btb}')
        
        # return the score
        return [cleared_rows, is_tspin, is_all_clear]
        # return self.calculate_score(cleared_rows, is_tspin, is_all_clear, 0, 0)
    
    def get_current_state(self):
        return self.field_data
    
    def get_follow_states(self, piece):
        """ Generates all possible next states that follow from the current state of the field. """
        next_states = []
        next_scores = []
        
        # rotate the piece in all possible directions
        for rot in range(piece.pdata.num_rot):            
            (ml, mr) = piece.pdata.margins[rot]
                        
            # move the piece to all possible positions
            for py in range(-ml, self.width - mr): 
                px = self.drop_piece(piece, rot, [0, py])
                dropped_pos = [px, py]
                
                # add the dropped piece as a new state
                self._append_state(next_states, next_scores, piece, rot, dropped_pos)
                
                # try kick/flip the piece with all possible rotations
                self._kick_expansion(piece, rot, dropped_pos, next_states, next_scores)
                
                
                # move the piece left/right and try to kick/flip it (enables t-spin triples, for example)
                left = 1
                while True:
                    if self.is_collision(piece, rot, [px, py - left]) or not self.is_collision(piece, rot, [px - 1, py - left]):
                        break
                    else:
                        left += 1
                        self._kick_expansion(piece, rot, [px, py - left], next_states, next_scores)
                
                right = 1
                while True:
                    if self.is_collision(piece, rot, [px, py + right]) or not self.is_collision(piece, rot, [px - 1, py + right]):
                        break
                    else:
                        right += 1
                        self._kick_expansion(piece, rot, [px, py + right], next_states, next_scores)
        
        # remove duplicates
        next_states, next_states_indices = np.unique(np.array(next_states).reshape(len(next_states), -1), axis=0, return_index=True)
        next_states = next_states.reshape((-1, 20, 10))
        
        next_scores = np.take(np.array(next_scores, dtype=object), next_states_indices, axis=0)
        
        return (next_states, next_scores)
    
    def _kick_expansion(self, piece, rot, dropped_pos, states, scores):
        (px, py) = self._extract_piece_info(piece, rot, dropped_pos)

        for kick_rot in range(piece.pdata.num_rot):
            (kick_succ, kick_result) = self._rotate(piece, rot, rot - kick_rot, dropped_pos)

            if kick_succ and self.is_collision(piece, kick_result[2], [px - 1, py]):
                # possible state
                dropped_px = self.drop_piece(piece, kick_result[2], [kick_result[0], kick_result[1]])
                
                self._append_state(states, scores, piece, kick_result[2], [dropped_px, kick_result[1]])
    
    
    def _append_state(self, states, scores, piece, rot, pos=None):
        new_state = self._add_piece_to_board(piece, rot, pos)
        score = self.handle_clears(new_state, piece, rot, pos)
        
        states.append(new_state)
        scores.append(score)
        
        # print('Score:', score)
        # self._print_board(new_state)
        # print()
        
    
    def _rotate(self, piece, rot, rot_offset, pos=None):
        """Tries to rotate the given piece (applying kicks/spins, if else not possible) and returns if the rotation worked and the new piece infos, as a tuple."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        to_rot = (rot + rot_offset) % piece.pdata.num_rot
        
        # if it does not collide, just rotate it
        if not self.is_collision(piece, to_rot, pos):
            return (True, (px, py, to_rot))
        
        # otherwise try to kick it
        table = i_kicks if piece.ptype == 4 else kicks
        
        return self._kick_piece(table, piece, rot, to_rot, pos)
        
        
    def _kick_piece(self, table, piece, rot, to_rot, pos=None):
        """Tries to kick the piece and returns if it was successful and the new piece infos, as a tuple."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        if not (rot, to_rot) in table:
            return (False, None)
        
        for x, y in table[rot, to_rot]:
            # for each offset, test if it's valid
            if not self.is_collision(piece, to_rot, [px + x, py + y]):
                # if it's vlaid, kick it and break
                return (True, (px + x, py + y, to_rot))
        
        return (False, None)
        
    
    def drop_piece(self, piece, rot, pos=None):
        """Tries to drop the given piece on this field and returns the height it landed on."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        while not self.is_collision(piece, rot, [px, py]):
            px += 1

        return px - 1
    
    def _add_piece_to_board(self, piece, rot, pos=None):
        """Places the piece on the board and returns the new resulting field."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        temp_field = np.copy(self.field_data)
        
        for x, y in piece.pdata.data[rot]:
            temp_field[x + px, y + py] = 1
        
        return temp_field
    
    def drop_piece_on_field(self, piece, rot, pos=None):
        """ Drops the given piece on this field, returning the newly generated field."""
        (px, py) = self._extract_piece_info(piece, rot, pos)
        
        px = self.drop_piece(piece, rot, pos)
        
        return self._add_piece_to_board(piece, rot, [px, py])
    
    
    def drop_piece_on_field_(self, piece, rot, pos=None):
        """ Drops the given piece on this field in-place."""
        self.field_data = self.drop_piece_on_field(piece, rot, pos)
    
    def _print_board(self, board):
        for row in board:
            print(''.join(map(lambda cell: ' ' if cell == 0 else '█', row)))
            
    def reset(self):
        self.field_data = np.zeros((self.height, self.width))
        
    def get_number_of_holes(self):
        
        holes = []
        
        for ci, column in enumerate(self.field_data.T):
            top = -1
            # print(f'column {ci}')
            
            for i in range(self.height):
                # print(f'   row {i}, top = {top}')
                if top == -1:
                    if column[i] == 0:
                        continue
                    else:
                        top = i
                else:
                    if column[i] == 0:
                        holes.append((i, ci))
        return holes
                
                
            
    
    def get_column_heights(self):
        '''Calculates the height of every column, maximum height and height difference between columns.'''
        max_height = 0
        heights = []
        height_diffs = []
        
        last_height = -1
        
        for column in self.field_data.T:
            h = 0
            while h < self.height and column[h] == 0:
                h += 1
            h = self.height - h
            
            if last_height >= 0:
                dif = h - last_height
                height_diffs.append(dif)
            
            last_height = h
            
            if h > max_height:
                max_height = h
                
            heights.append(h)
        
        return (heights, max_height, height_diffs)
        
        
    def __str__(self):
        return str(self.field_data)
    
    def __repr__(self):
        return self.__str__()