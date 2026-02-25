import random
from math import pi, sin, cos
import matplotlib.pyplot as plt

def random_walk_demo():
    for i in range(50):
        x, y = randomwalk(1, 100000)

        plt.plot(x, y, color=(random.random(), random.random(), random.random()))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Random walk")
    plt.show()

def randomwalk(L,N):

    x= [0]
    y = [0]

    for i in range(N):
        theta = 2*pi*random.random()
        dx = L*cos(theta)
        dy = L*sin(theta)
        x.append(x[-1]+dx)
        y.append(y[-1]+dy)

    return x, y

random_walk_demo()
