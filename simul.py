from planets import Planet
from math import *
from itertools import permutations

class Simulation():
    def __init__(self, nPlanets = 3, planetMasses = (40.,10.,25.), planetPositions = [[100,0], [-50, 86.6025], [-50, -86.6025]], startingVelocities= [[0.,1.2], [-1, -0.6124], [1, -0.6124]]):
        self.nPlanets = nPlanets
        self.planets = [Planet(planetPositions[i], planetMasses[i], startingVelocities[i]) for i in range(nPlanets)]
        self.G = 10.#6.6743e-11
        
    def get_vector_acceleration_A_to_B(self, planetA:Planet, planetB:Planet):
        distX = planetB.pos[0] - planetA.pos[0]
        distY = planetB.pos[1] - planetA.pos[1]
        r = sqrt((distX**2) + (distY**2))
        a = (self.G*planetB.m)/r**2
        δx = a*(distX/r)
        δy = a*(distY/r)
        return [δx, δy]
    
    def update(self):
        accelerationChanges = [[0,0] for _ in range(self.nPlanets)]
        
        for planetA, planetB in permutations(self.planets, 2):
            acceleration = self.get_vector_acceleration_A_to_B(planetA, planetB)
            index = self.planets.index(planetA) 
            accelerationChanges[index] = list(map(lambda x, y: x + y, accelerationChanges[index], acceleration))
            
        for i,planet in enumerate(self.planets):
            planet.vel = list(map(lambda x,y:x+y, accelerationChanges[i], planet.vel))

            planet.step()