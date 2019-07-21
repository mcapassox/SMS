import numpy as np
from prey import Prey
from predators import Predator
from scipy import spatial
import time
from celluloid import Camera
from matplotlib import pyplot as plt
from utils import *
import _thread


def plotty(time_vec, n_prey_vec_total, n_pred_vec_total, n_prey_vec, n_pred_vec):

    plt.title("Populations vs time")
    plt.xlabel("Elapsed time (#)")
    plt.ylabel("# of individuals")
    plt.plot(time_vec,n_prey_vec_total, label='Preys')
    plt.plot(time_vec,n_pred_vec_total, label='Predators')

    for i in range(n_sim):
        plt.plot(time_vec,n_prey_vec[i], alpha=0.2)
        plt.plot(time_vec,n_pred_vec[i], alpha=0.2)

    plt.legend()
    plt.savefig('sim.pdf')
    plt.close()


def input_thread(a_list):
    input()
    a_list.append(True)

def single_sim(value):

    a_list = []
    n_pred_vec = []
    n_prey_vec = []
    time_vec = []

    width = 1000
    height = 1000
    n_flock = 600
    n_pred = 25

    elapsed = 0

    flock = [Prey(*np.random.rand(2)*1000, width, height, np.mod(_,2)) for _ in range(n_flock)]
    predators = [Predator(*np.random.rand(2)*1000, width, height,np.mod(_,2)) for _ in range(n_pred)]

    _thread.start_new_thread(input_thread, (a_list,))

    while flock and predators and len(flock) < 2000 and elapsed < len_sim and not a_list:

        pointmap = create_map(flock)

        locations = np.array(list(pointmap.keys()))
        tree = spatial.KDTree(locations, 15)
        all = flock + predators

        for boid in all:
            boid.apply_behaviour(flock, tree, locations, pointmap, predators, elapsed)

        for boid in all:
            boid.update()
            boid.edges()

        print(len(flock),",", len(predators),",",elapsed)
        n_prey_vec.append(len(flock))
        n_pred_vec.append(len(predators))
        time_vec.append(elapsed)

        elapsed += 1

    #plt.title("Populations vs time")
    #plt.xlabel("Elapsed time (#)")
    #plt.ylabel("# of individuals")
    #plt.plot(time_vec,n_prey_vec, label='Preys')
    #plt.plot(time_vec,n_pred_vec, label='Predators')

    #plt.legend()
    #plt.savefig('sim_{}.pdf'.format(value))
    #plt.close()
    return n_prey_vec, n_pred_vec

len_sim = 2000

total_prey = np.zeros((len_sim,2))
total_pred = np.zeros((len_sim,2))
time_vec = np.linspace(0,len_sim,len_sim)
time_vec = time_vec.reshape((len_sim))
n_sim = 20

for value in range(n_sim):

    n_prey_vec, n_pred_vec = single_sim(value)

    n_prey_vec = np.pad(n_prey_vec, (0,len_sim - len(n_prey_vec)), 'constant', constant_values=(0, 0)).reshape((1,len_sim))
    n_pred_vec = np.pad(n_pred_vec, (0,len_sim - len(n_pred_vec)), 'constant', constant_values=(0, 0)).reshape((1,len_sim))

    if value != 0:
        total_prey = np.concatenate((total_prey, n_prey_vec), axis = 0)
        total_pred = np.concatenate((total_pred, n_pred_vec), axis = 0)
    else:
        total_prey = n_prey_vec
        total_pred = n_pred_vec


for i in range(n_sim):
    for j in range(len_sim):
        if total_prey[i][j] == 0:
            total_prey[i][j] = total_prey[i-1][j]

for i in range(n_sim):
    for j in range(len_sim):
        if total_pred[i][j] == 0:
            total_pred[i][j] = total_pred[i-1][j]

total_prey_mean = np.mean(total_prey, axis = 0)
total_pred_mean = np.mean(total_pred, axis = 0)
print("\n")


plotty(time_vec, total_prey_mean, total_pred_mean, total_prey, total_pred)
