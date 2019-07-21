from scipy import spatial
import numpy as np
import collections
from boid import Boid
from utils import *

class Predator(Boid):

    def __init__(self, x, y, width, height, sex):
        Boid.__init__(self, x,y,width, height, sex)

        self.max_force_coe = 2
        self.max_speed = 13

        self.perception = 75
        self.lastate = 0
        self.radius = 5
        self.color = 'r'
        self.sex = sex

        self.eat_counter = 0
        self.velocity = (np.random.rand(2) - 0.5)*10



    def eat(self, position, range):
        range.pop(position)
        self.eat_counter += 1


    def apply_behaviour(self, boids, tree, locations, pointmap, predators, time):

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
            if norm(self.position - boid.position, 2) < 10 :
                self.eat(boids.index(boid), boids)
