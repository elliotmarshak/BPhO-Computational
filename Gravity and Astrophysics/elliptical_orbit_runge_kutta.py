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

x0 = a * (1-e)
y0 = 0.0 #the position is stored as a vector relative to the centre. this formula will start the planet at the perihelion
vx0 = 0.0
vy0 = sqrt(G * M * (1+e) / (a * (1-e))) #formula for the starting velocity at the perihelion

state = np.array([x0, y0, vx0, vy0])

def acceleration(r):
    norm = np.linalg.norm(r)
    return -G * M * r / norm ** 3 #vector formula for the acceleration in an elliptical orbit

def derivatives(state):
    x, y, vx, vy = state
    ax, ay = acceleration(np.array([x, y]))
    return np.array([vx, vy, ax, ay])

def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

x_positions = []
y_positions = []

for i in range(steps):
    state = rk4_step(state, dt)
    x_positions.append(state[0])
    y_positions.append(state[1])

x_positions = np.array(x_positions)
y_positions = np.array(y_positions)

fig = plt.figure()
ax = plt.subplot()
ax.set_aspect("equal")
ax.set_xlim(-1.5 * a, 1.5 * a)
ax.set_ylim(-1.5 * a, 1.5 * a)
ax.set_title("Simple Elliptical Orbit using Runge-Kutta Method")
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
