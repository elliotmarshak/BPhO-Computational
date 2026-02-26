import numpy as np
from numpy import pi, cos, sin, sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 4 * pi**2 #G when using units of AU, solar masses and years
M = 1.0 #the mass of the sun

a = 1.0 #semi major axis length in AU
e = 0.5 #eccentricity

b = a*sqrt(1-e**2)

time_period = (2*pi*a**(3/2))/(sqrt(G*(M))) #find time period using Kepler II

steps = 10000 #steps
dt = 0.001 #each discrete time step
newton_raphson_iterations = 10 #iterations for newtons method to solve kepler equation

r = np.array([a * (1-e), 0]) #the position is stored as a vector relative to the centre. this formula will start the planet at the perihelion
t = 0 #time

x_positions = []
y_positions = []

def kepler(M, E, e):
    return E - e * sin(E) - M
    #can easily solve roots of equation to find the eccentric anomaly

def kepler_derivative(E, e):
    #f'(E) = 1 - e * cos(E)
    return 1 - e * cos(E)

def solve_kepler(mean_anomaly, e):
    #uses newton raphson method to find the eccentric anomaly from Kepler's equation
    eccentric_anomaly = mean_anomaly
    for i in range(newton_raphson_iterations):
        eccentric_anomaly = eccentric_anomaly - kepler(mean_anomaly, eccentric_anomaly, e) / kepler_derivative(eccentric_anomaly, e)
    return eccentric_anomaly

def get_orbit_angle(mean_anomaly, e):
    #finds the true anomaly given the mean anomaly, the semi major axis and the eccentricity using Kepler's equation
    eccentric_anomaly = solve_kepler(mean_anomaly, e)

    true_anomaly = 2 * np.arctan(sqrt((1+e)/(1-e)) * np.tan(eccentric_anomaly / 2))

    return true_anomaly

for i in range(steps):
    #precalculate the positions in the orbit
    t += dt
    mean_anomaly = 2*pi*((t % time_period)/time_period)
    angle = get_orbit_angle(mean_anomaly, e)

    radius = (a*(1-e**2))/(1+e*cos(angle))

    x = radius * cos(angle)
    y = radius * sin(angle)

    x_positions.append(x)
    y_positions.append(y)

x_positions = np.array(x_positions)
y_positions = np.array(y_positions)

fig = plt.figure()
ax = plt.subplot()
ax.set_aspect("equal")
ax.set_xlim(-1.5 * a, 1.5 * b)
ax.set_ylim(-1.5 * a, 1.5 * a)
ax.set_title("Simple Elliptical Orbit using Newton's Method for solving Kepler Equation")
ax.set_xlabel("x / AU")
ax.set_ylabel("y / AU")

ax.plot(0,0, color="yellow", marker="o", markersize=10)
ax.plot(x_positions, y_positions, color="blue", alpha=0.3)

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

print(f"Time Period: {round(time_period, 2)} years")

plt.show()