from scipy import spatial
import numpy as np
from boid import Boid
import ray
from utils import *

class Prey(Boid):

    def __init__(self, x, y, width, height):
        Boid.__init__(self, x, y, width, height)

        self.max_force_coe = 0.7
        self.max_force_sep = 1
        self.max_force_esc = 10

        self.max_speed = 7
        self.perception = 50

        self.velocity = (np.random.rand(2) - 0.5)*self.max_speed
        
        self.radius = 2
        self.color = 'b'


    def apply_behaviour(self, boids, tree, locations, pointmap, predators):

        indices = getNearestPoint(tree, [self.position[0], self.position[1]], locations)
        indices = np.delete(indices,0)

        if indices.size - 1 :
            range = [point for near_loc in locations[indices]
                       for point in pointmap[tuple(near_loc)]]

            COM = locations[indices].mean(axis = 0)

            cohesion = self.cohesion(range,COM)
            alignment = self.align(range)
            separation = self.separation(range)

            self.acceleration += cohesion
            self.acceleration += (alignment)
            self.acceleration += (separation)

            self.reproduce(boids, range)


        borders = self.borders()
        pred = self.run_away(predators)

        self.acceleration += borders
        self.acceleration += pred

    def align(self, boids):
        steering = np.zeros(2)
        total = 0
        avg_vector = np.zeros(2)

        for boid in boids:
            avg_vector += boid.velocity
            total += 1

        mag = norm(avg_vector, 2)
        if total > 0 and mag != 0:
            avg_vector /= total
            avg_vector = (avg_vector / norm(avg_vector, 2)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering


    def separation(self, boids):
        steering = np.zeros(2)
        for boid in boids:
            distance = norm(self.position - boid.position,2)
            if distance < self.perception/2:
                steering -= (boid.position - self.position)
        mag = norm(steering,2)
        if mag > self.max_force_sep:
            steering = (steering /mag) * self.max_force_sep

        return steering


    def run_away(self, predators):
        steering = np.zeros(2)
        for pred in predators:
            distance = self.position-pred.position
            mag = norm(distance,2)
            if(mag < self.perception):
                if mag != 0:
                    steering += (distance/mag) * self.max_force_esc
        return steering

    def reproduce(self, boids, range):
        if np.random.randint(0,52) < 1:
            x = np.random.randint(0, self.perception/2) - self.perception + self.position[0]
            y = np.random.randint(0, self.perception/2) - self.perception + self.position[1]

            newborn = Prey(x,y, self.width, self.height)
            boids.append(newborn)
