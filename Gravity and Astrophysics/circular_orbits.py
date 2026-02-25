from random import random
import numpy as np
from numpy import pi, cos, sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation

r_earth = 1
r_mars = 1.523
P_earth = 1
P_mars = (r_mars/r_earth)**1.5 #Kepler III

time_series = np.linspace(0, 5 * P_mars, 1000)
theta_earth = 2 * pi * random() + 2 * pi * time_series / P_earth
theta_mars = 2 * pi * random() + 2 * pi * time_series / P_mars

x_earth, y_earth = r_earth * cos(theta_earth), r_earth * sin(theta_earth)
x_mars, y_mars = r_mars * cos(theta_mars), r_mars * sin(theta_mars)

fig = plt.figure()
ax = fig.add_subplot()
plt.title("Simple Circular Orbit")
plt.xlabel("X / AU")
plt.ylabel("Y / AU")

#fix axis to a square to avoid stretching
ax.set_aspect("equal", adjustable="box")
limit = r_mars + 0.2
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)

#paths of the orbit
ax.plot(x_earth, y_earth, color="blue", alpha=0.35)
ax.plot(x_mars, y_mars, color="orange", alpha=0.35)

#Sun
ax.plot(0, 0, marker="o", color="gold", markersize=10)

#moving planets
earth_dot, = ax.plot([], [], "o", color="blue", markersize=8, label="Earth")
mars_dot, = ax.plot([], [], "o", color="orange", markersize=8, label="Mars")
ax.legend(loc="upper right")

def update(frame):
	earth_dot.set_data([x_earth[frame]], [y_earth[frame]])
	mars_dot.set_data([x_mars[frame]], [y_mars[frame]])
	return earth_dot, mars_dot


ani = animation.FuncAnimation(
	fig,
	update,
	frames=len(time_series),
	interval=20,
	blit=True,
	repeat=True,
)

plt.show()
