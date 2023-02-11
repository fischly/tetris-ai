import numpy as np
import random

from tetris.Piece import Piece
from tetris.Bag import Bag
from tetris.Field import Field
from tetris.Scoring import SCORING


class TetrisEnv():
    def __init__(self):
        self.field = Field()
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
        
        
    def get_next_states(self):
        '''Returns all possible follow states by placing the current piece at (nearly) all possible positions.'''
        next_states, next_clears = self.field.get_follow_states(Piece(self.current_piece))
        # current_states = [self.field.get_current_state() for _ in range(len(next_states))]
        scores = [SCORING['GAME_OVER'] if clear is None else self._calculate_score(*clear, self.current_combo, self.current_btb) for clear in next_clears]
        dones = [clear is None for clear in next_clears]
        queue = []
        
        return (next_states, scores, next_clears, dones)
    
    def get_current_state(self):
        return self.field.get_current_state()
    
    def get_next_queue(self, length=5):
        return self.bag.peek_pieces(length)
    
    
    def step(self, next_state, next_clear, next_score):
        self.field.field_data = next_state
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
            
        self.moves += 1
        
    
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
        