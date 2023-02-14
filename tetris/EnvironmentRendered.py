import numpy as np
import random

from tetris.Piece import Piece
from tetris.Bag import Bag
from tetris.FieldRendered import FieldRendered
from tetris.Scoring import SCORING


class TetrisEnvRendered():
    def __init__(self):
        self.field = FieldRendered()
        self.bag = Bag()
        
        self.current_piece = self.bag.next_piece()
        self.hold_piece = None
        
        self.current_combo = 1
        self.current_btb = 1
        
        # game statistics
        self.score = 0
        self.moves = 0
        self.clears = [0, 0, 0, 0]
        self.tspins = 0
        self.all_clears = 0
        self.max_combo = 0
        self.max_btb = 0
        
        # amount of lines cleared by last piece
        self.last_move_lines_cleared = 0
        # score done by last piece
        self.last_move_score = 0
        
        
    def get_next_states(self, use_hold=False):
        '''Returns all possible follow states by placing the current piece at (nearly) all possible positions.'''
        if use_hold and self.hold_piece is None:
            piece_to_use = self.bag.peek_piece()
        elif use_hold:
            piece_to_use = self.hold_piece
        else:
            piece_to_use = self.current_piece
        
        next_states, next_states_pretty, next_clears, next_heuristics, next_moves = self.field.get_follow_states(Piece(piece_to_use))

        scores = [SCORING['GAME_OVER'] if clear[0] == -1 else self._calculate_score(*clear, self.current_combo, self.current_btb) for clear in next_clears]
        dones = [clear[0] == -1 for clear in next_clears]
        
        # add environment specific heuristics
        env_heuristics = self.get_heuristics()
        
        combined_heuris = np.zeros((next_heuristics.shape[0], 25))
        combined_heuris[:, :next_heuristics.shape[1]] = next_heuristics
        combined_heuris[:, next_heuristics.shape[1]:] = np.broadcast_to(env_heuristics, (next_heuristics.shape[0], len(env_heuristics)))
        
        return (next_states, next_states_pretty, scores, next_clears, combined_heuris, dones, next_moves)
      
    
    def get_current_state(self):
        return self.field.get_current_state()
    
    def get_current_state_pretty(self):
        return self.field.get_current_state_pretty()
    
    def get_next_queue(self, length=5):
        return self.bag.peek_pieces(length)
    
    
    def step(self, next_state, next_state_pretty, next_clear, next_score):
        self.field.field_data = next_state
        self.field.field_data_pretty = next_state_pretty
        
        self.current_piece = self.bag.next_piece()
        
        cleared_rows = next_clear[0]
        is_tspin = next_clear[1]
        is_all_clear = next_clear[2]
        
            
        # update back-to-back
        if is_tspin or cleared_rows == 4:
            self.current_btb += 1
        elif cleared_rows > 0:
            self.current_btb = 1
        
        # update combo
        if cleared_rows > 0:
            self.current_combo += 1
            self.clears[cleared_rows - 1] += 1
        else:
            self.current_combo = 1
            
        # update this run's score
        self.score += next_score
        
        if is_tspin:
            self.tspins += 1
        if is_all_clear:
            self.all_clears += 1
            
        if self.current_btb > self.max_btb:
            self.max_btb = self.current_btb
        if self.current_combo > self.max_combo:
            self.current_combo = self.max_combo
            
        self.moves += 1
        
        self.last_move_lines_cleared = cleared_rows
        self.last_move_score = next_score
        
    def hold(self):
        if self.hold_piece is not None:
            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
        else:
            self.hold_piece = self.current_piece
            self.current_piece = self.bag.next_piece()
    
    def _calculate_score(self, cleared_lines, t_spin, all_clear, combo, btb):
        """Calculates the score by considering the number of cleared lines, whether a t-spin was performed and the current combo and back-to-back streaks."""
        # get base score
        score = SCORING['TSPIN' if t_spin else 'NORMAL'][cleared_lines]

        if cleared_lines > 0 and btb > 1:
            score *= SCORING['BACKTOBACK_MULTIPLIER'] * (btb / 2)

        if combo > 1:
            score += SCORING['COMBO'] * (combo - 1)

        if all_clear:
            score += SCORING['ALL_CLEAR']

        return score
    
    def _print_state(self, s):
        self.field._print_board(s)
    def _print_current_state(self):
        self._print_state(self.get_current_state())
        
    def reset(self):
        self.field.reset()
        self.bag.reset()
        
        self.current_piece = self.bag.next_piece()
        
        self.current_combo = 1
        self.current_btb = 1
        
        self.score = 0
        self.moves = 0
        self.clears = [0, 0, 0, 0]
        self.tspins = 0
        self.all_clears = 0
        
    
    def get_heuristics(self):
        
        I_pieces, T_pieces = self.get_number_of_pieces()
        
        return [
            self.last_move_lines_cleared,
            self.last_move_score,
            I_pieces,
            T_pieces
        ]
    
    def get_number_of_pieces(self):
        pieces = self.bag.peek_pieces(5)
        
        I_counter = 0
        T_counter = 0
        
        for piece in pieces:
            if piece == 0:
                T_counter += 1
            elif piece == 4:
                I_counter += 1
        
        return (I_counter, T_counter)