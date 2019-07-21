import numpy as np
from prey import Prey
from predators import Predator
from scipy import spatial
import time
from celluloid import Camera
from matplotlib import pyplot as plt
from utils import *

def photoshoot():

    for value in range(1):

        width = 1000
        height = 1000
        n_flock = 1000
        #n_pred = int(n_flock/25)
        n_pred = 5
        elapsed = 0

        flock = [Prey(*np.random.rand(2)*1000, width, height, np.mod(_,2)) for _ in range(n_flock)]
        predators = [Predator(*np.random.rand(2)*1000, width, height, np.mod(_,2)) for _ in range(n_pred)]

        fig = plt.figure()
        camera = Camera(fig)

        while flock and predators and len(flock) < 1100 and elapsed < 300:

            start = time.perf_counter()
            color = []
            radius = []

            x = np.empty(len(flock+predators))
            y = np.empty(len(flock+predators))
            u = np.empty(len(flock+predators))
            v = np.empty(len(flock+predators))

            pointmap = create_map(flock)

            locations = np.array(list(pointmap.keys()))
            tree = spatial.KDTree(locations, 15)
            all = flock + predators

            for boid in all:
                boid.apply_behaviour(flock, tree, locations, pointmap, predators, elapsed)

            count = 0
            for boid in all:
                boid.update()
                boid.edges()

                x[count], y[count] = get_pos(boid.position)
                u[count], v[count] = get_vel(boid.velocity)

                color.append(boid.color)
                radius.append(boid.radius)
                count += 1

            plt.quiver(x,y,u,v, color = color)
            plt.scatter(x,y, c = color, s = radius)
            camera.snap()
            end = time.perf_counter()
            print(len(flock), len(predators), elapsed)
            print(end-start)
            elapsed += 1

        anim = camera.animate()
        anim.save("{}_300_5pred.mp4".format(value), writer = 'imagemagick')

def single_sim():

    width = 1000
    height = 1000
    n_flock = 1000
    n_pred = 10
    elapsed = 0

    flock = [Prey(*np.random.rand(2)*1000, width, height, np.mod(_,2)) for _ in range(n_flock)]
    predators = [Predator(*np.random.rand(2)*1000, width, height, np.mod(_,2)) for _ in range(n_pred)]


    while flock and predators and len(flock) < 1500 and elapsed < 10:

        pointmap = create_map(flock)

        locations = np.array(list(pointmap.keys()))
        tree = spatial.KDTree(locations, 15)
        all = flock + predators

        for boid in all:
            boid.apply_behaviour(flock, tree, locations, pointmap, predators, elapsed)

        for boid in all:
            boid.update()
            boid.edges()

        print(len(flock),",", len(predators),",", elapsed)
        elapsed += 1


#collect_data()
photoshoot()
#single_sim()
