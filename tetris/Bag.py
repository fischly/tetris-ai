import random
import math

# Bag mechanic from Tetr.io
# https://github.com/Poyo-SSB/tetrio-bot-docs/blob/master/Piece_RNG.md

class Bag():
    def __init__(self, seed=None):
        if seed is None:
            seed = random.randint(0, 2**32)
        self.reset(seed)
    
    def _next(self):
        self._t = 16807 * self._t % 2147483647
        return self._t
    
    def _nextFloat(self):
        return (self._next() - 1) / 2147483646
    
    def _shuffleList(self, l):
        if len(l) == 0:
            return l
        
        for i in range(len(l) - 1, 0, -1):
            r = math.floor(self._nextFloat() * (i + 1))
            l[i], l[r] = l[r], l[i]
        
        return l
    
    def _extend_bag(self):
        # new_bag = self._shuffleList(['z', 'l', 'o', 's', 'i', 'j', 't'])
        new_bag = self._shuffleList(list(range(7)))
        self.bag.extend(new_bag)
        
    
    def next_piece(self):
        if len(self.bag) <= 7:
            self._extend_bag()
        
        return self.bag.pop(0)
    
    def next_pieces(self, amount=7):
        # make sure there are enough elements in the bag
        while len(self.bag) <= amount + 7:
            self._extend_bag()
        
        # take the first 'amount' elmenents from the bag
        to_return = self.bag[:amount]
        self.bag = self.bag[amount:]
        
        return to_return
    
    def peek_piece(self):
        return self.bag[0]
    
    def peek_pieces(self, amount=7):
        # make sure there are enough elements in the bag
        while len(self.bag) <= amount + 7:
            self._extend_bag()
            
        return self.bag[:amount]
    
    def reset(self, new_seed=None):
        if new_seed is not None:
            self._t = new_seed % 2147483647

            if self._t <= 0:
                self._t += 2147483646
            
        self.bag = []
        self._extend_bag()
        