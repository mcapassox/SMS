import numpy as np
import ray
from utils import norm

class Boid():
    def __init__(self, x, y, width, height):

        self.max_force_esc = 9
        self.max_force_bor = 3

        self.width = width
        self.height = height

        self.position = np.array([x,y])
        self.acceleration = (np.random.rand(2) - 0.5)/2


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        mag = norm(self.velocity,2)
        if mag > self.max_speed:
            self.velocity = self.velocity / mag * self.max_speed

        self.acceleration = np.zeros(2)

    def edges(self):
        if self.position[0] > self.width:
            self.position[0] = 0
            self.velocity[0] *= -1
        elif self.position[0] < 0:
            self.position[0] = self.width
            self.velocity[0] *= -1

        if self.position[1] > self.height:
            self.position[1] = 0
            self.velocity[1] *= -1
        elif self.position[1] < 0:
            self.position[1] = self.height
            self.velocity[1] *= -1

    #@ray.remote
    def cohesion(self, boids, center_of_mass):

        steering = np.zeros(2)
        vec_to_com = center_of_mass - self.position
        mag = norm(vec_to_com, 2)
        if mag > 0:
            vec_to_com = (vec_to_com / mag) * self.max_speed

        steering = vec_to_com - self.velocity

        mag = norm(steering,2)
        if mag > self.max_force_coe:
            steering = (steering /mag) * self.max_force_coe

        return steering


    def borders(self):
        steering = np.zeros(2)
        distance = np.array([self.width/2,self.height/2]) - self.position
        mag = norm(distance, 4)
        if(mag > self.width/2 - 20):
                steering = (distance/norm(distance,2)) * self.max_force_bor
        return steering
