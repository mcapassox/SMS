from scipy import spatial
import numpy as np
import collections
from boid import Boid
from utils import *

class Predator(Boid):

    def __init__(self, x, y, width, height):
        Boid.__init__(self, x, y, width, height)

        self.max_force_coe = 3
        self.max_speed = 15

        self.velocity = (np.random.rand(2) - 0.5)*self.max_speed

        self.perception = 30
        self.radius = 5
        self.color = 'r'
        self.eat_counter = 0



    def eat(self, position, range):
        range.pop(position)
        self.eat_counter += 1



    def apply_behaviour(self, boids, tree, locations, pointmap, predators):

        #indices = getNearestPoint_Radius(tree, [self.position[0], self.position[1]], self.perception)
        indices = getNearestPoint(tree, [self.position[0], self.position[1]], locations)

        range = [point for near_loc in locations[indices]
                       for point in pointmap[tuple(near_loc)]]

        if range:
                COM = locations[indices].mean(axis = 0)
                if len(COM)>1:
                    COM = min(locations[indices], key=lambda p: sum((p - COM)**2))
                    cohesion = self.cohesion(range, COM)
                    self.acceleration += cohesion

        borders = self.borders()
        self.acceleration += borders

        for boid in boids:
            if norm(self.position - boid.position, 2) < 12 :
                self.eat(boids.index(boid), boids)

        self.die(boids,predators)
        if(self.eat_counter > 5):
            self.reproduce(predators)
            self.eat_counter = 0

    def die(self, preys, predators):
        p = 1
        if np.random.randint(0,83) <  p:
            predators.pop(predators.index(self))


    def reproduce(self, boids):
        x = np.random.randint(0, self.perception/2) - self.perception + self.position[0]
        y = np.random.randint(0, self.perception/2) - self.perception + self.position[1]

        newborn = Predator(x,y, self.width, self.height)
        boids.append(newborn)
