from random import random
import numpy as np
from numpy import pi, cos, sin, sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 4 * pi**2 #G when using units of AU, solar masses and years
M = 1.0 #the mass of the sun

a = 1.0 #semi major axis length in AU
e = 0.4 #eccentricity

dt = 0.001
steps = 20000 #steps for verlet method

r = np.array([a * (1-e), 0]) #the position is stored as a vector relative to the centre. this formula will start the planet at the perihelion
vel = np.array([0, sqrt(G * M * (1+e) / (a * (1-e)))]) #formula for the starting velocity at the perihelion

def acceleration(r):
    norm = np.linalg.norm(r)
    return -G * M * r / norm ** 3 #vector formula for the acceleration in an elliptical orbit

acc = acceleration(r)

x_positions = []
y_positions = []

for i in range(steps):
    r += vel * dt + 0.5 * acc * dt**2 #simply using s = ut + 1/2at^2
    acc_new = acceleration(r)
    vel += 0.5 * (acc + acc_new) * dt #we use the average of the accelerations and then use v = u + at
    acc = acc_new
    x_positions.append(r[0])
    y_positions.append(r[1])

x_positions = np.array(x_positions)
y_positions = np.array(y_positions)

fig = plt.figure()
ax = plt.subplot()
ax.set_aspect("equal")
ax.set_xlim(-1.5 * a, 1.5 * a)
ax.set_ylim(-1.5 * a, 1.5 * a)
ax.set_title("Simple Elliptical Orbit using Verlet Method")
ax.set_xlabel("x / AU")
ax.set_ylabel("y / AU")

ax.plot(0,0, color="yellow", marker="o", markersize=10)
ax.plot(x_positions, y_positions, color="blue", alpha=0.3)

ax.plot(0, 0, marker="o", color="gold", markersize=10)

planet_dot, = ax.plot([], [], color = "blue", marker = "o", markersize=6)

def update(frame):
    planet_dot.set_data([x_positions[frame]], [y_positions[frame]])
    return planet_dot,

anim = animation.FuncAnimation(
    fig, 
    update, 
    frames=len(x_positions), 
    interval=20,
    repeat=True
)

plt.show()
