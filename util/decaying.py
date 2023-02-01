class Decaying():
    def __init__(self, start, end, duration):
        self.per_step = (end - start) / duration
        self.duration = duration
        self.current_step = 0
        self.current = start
        

    def step(self):
        if self.current_step < self.duration:
            self.current += self.per_step
            self.current_step += 1
            
        return self.current
    
    def get(self):
        return self.current

class DecayingFunc():
    def __init__(self, func):
        self.func = func
        self.current_step = 0
        
    def step(self):
        self.current_step += 1
        return self.func(self.current_step)
    
    def get(self):
        return self.func(self.current_step)

class DecayingLinear(DecayingFunc):
    def __init__(self, start, end, duration):
        step = (end - start) / duration
        
        f = lambda x: start + step * x if x < duration else end
        
        super().__init__(f)
    
class DecayingDiscount(DecayingFunc):
    def __init__(self, start, end, duration):
        factor = (1/(1-start))
        addition = start - (1 - end) 
        
        f = (lambda x: ((x/duration)**0.6)/factor + addition if (x/duration) < 1 else end)
        
        super().__init__(f)