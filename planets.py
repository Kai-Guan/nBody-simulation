from random import randint

class Planet():
    def __init__(self, pos:list[float,float], m:float, vel:list[float,float]):
        #pos
        self.pos : list[float, float] = pos
        
        #mass
        self.m : float = m
        
        #velocity
        self.vel : list[float, float] = vel
        
        self.trail = []
        self.trailLen = 0
        
        self.col = [randint(0, 255) for _ in range(3)]
        
    def add_history(self,pos):
        
        self.trailLen += 1
        if pos not in self.trail:
            self.trail.append(pos)
        if self.trailLen > 250:
            self.trailLen -= 1
            self.trail.pop(0)
        
    def step(self):
        self.add_history(self.pos)
        self.pos = list( map(lambda x,y:x+y, self.pos, self.vel))