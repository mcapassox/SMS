from scipy import spatial
import collections
import numpy as np
from scipy.integrate import odeint
import pandas as pd

from lmfit import minimize, Parameters, Parameter, report_fit

def norm(vector, pow):
    out = (vector[0]**pow+vector[1]**pow)**(1/pow)
    return out

def getNearestPoint_Radius(tree, point, radius):
    indices = tree.query_ball_point(point, radius)
    return indices

def getNearestPoint(tree, point, loc):
    if len(loc) > 5:
        list2, indices = tree.query(point, 5)
    else:
        list2, indices = tree.query(point, len(loc))
    return indices

def create_map(flock):
    pointmap   = collections.defaultdict(list)
    for boid in flock:
        pointmap[boid.position[0], boid.position[1]].append(boid)
    return pointmap

def get_pos(vec):
    x = vec[0]
    y = vec[1]
    return x,y

def get_vel(vec):
    u = vec[0]
    v = vec[1]
    return u,v
