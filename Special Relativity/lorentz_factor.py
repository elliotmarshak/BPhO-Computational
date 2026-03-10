import numpy as np
import matplotlib.pyplot as plt

def lorentz_factor(v):
    # Calculate lorentz factor given velocity of moving object as a fraction of c
    return 1/np.sqrt(1-v**2)

v = np.linspace(0, 0.99, 1000) # Velocity of moving object as a fraction of c
gamma = lorentz_factor(v)

plt.figure()
plt.plot(v, gamma, color="blue", linewidth=2)

plt.xlabel("v/c", fontsize=12)
plt.ylabel("Lorentz Factor", fontsize=12)
plt.title("Plot of Lorentz Factor vs v (as fraction of c)", fontsize=14)

plt.show()