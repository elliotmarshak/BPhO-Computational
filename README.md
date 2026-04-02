# BPhO-Computational
A collection of projects for simulating various physics problems from the British Physics Olympiad Computational
 ## Kinematics
 ### Bouncing Ball
 From the second lecture (Kinematics). This models a simple ball moving up and down by using a coefficient of restitution.

 ### Balls in a Box
 Also from the second lecture, this one took a bit more work. The collisions now occur in 2D and 2 balls of different masses are dropped from slightly different locations and are allowed to bounce around the box, with acceleration due to gravity acting on them, as well as a fixed coefficient of restitution. The 2D collisions are easily broken down into a 1D problem along a collision axis by using the dot product to project the velocities onto this axis. Then, the Zero Momentum Frame is used to easily calculate the velocities after the collision. Some correction logic is also needed to deal with the errors of ball overlap caused by discrete time.
![balls_in_box](https://github.com/user-attachments/assets/d695729c-ca4d-4b91-b27f-944a7480b4d2)

## Gravity and Astrophysics
### Eccentric Orbits
This was from the Gravity and Astrophysics lecture. First I made a simple circular orbit of a planet orbitting a central body. I just used a simple uniform rate of change of angle and found the position using trigonometry. For the elliptical orbits, I used 3 different methods to calculate the positions with respect to time. First I used the Verlet Method to assume constant acceleration between discrete time steps. For the second one, I used the Runge-Kutta method to calculate the position. Finally I used the Newton-Raphson method to solve the Kepler equation to find the eccentric anomaly. Then the true anomaly (theta) can be found and the position can be calculated using the elliptic formula for r in terms of theta.

## Waves and Optics
 ### Double Slit and Diffraction Simulation
 This project is a numerical simulation of wave interference and diffraction. It shows both the propagation of waves in 2D space and the resulting intensity pattern on a screen. Parameters like the wavelength, slit separation, slit width, and number of slits can be adjusted interactively.

Finite-width slits are approximated using a discrete set of sources. Each point source emits a spherical wave. The simulation uses complex exponentials to efficiently compute the wave contribution from each source at every point, and then sums these to get the total field.

The total wave field is calculated as:

$$\phi_{\rm total}(x, y, t) = \sum_{n=1}^{N} \frac{e^{i(k r_n - \omega t)}}{r_n}$$

where $r_n$ is the distance from source $n$ to the point $(x, y)$

The intensity measured on the screen is then $I(x) = {\vert \phi_{total}(x, y_{screen}, t) \vert}^2 $

<img width="699" height="398" alt="image" src="https://github.com/user-attachments/assets/308370ff-9ac3-4b44-8e3a-85cdc9dc9dd5" />

### FFT Frequency Analyser
I made a simple program where you can record audio from your microphone and have a spectrogram produced which shows the different frequencies present in the sample over time. It works by splitting the recording into overlapping frames, and then a Hann window (smoothly reduces signal to zero at obth ends) is applied to each frame which reduces spectral leakage (where sharp jumps/discontinuities are treated as high frequency components). Then a Fast Fourier Transform (FFT) is applied to each frame and finally I converted the magnitudes from the FFT to decibels and then plotted it on a spectrogram using a colour map.

<img width="550" height="430" alt="image" src="https://github.com/user-attachments/assets/9545f219-21db-4a3b-8a1f-b7edb5ce1db2" />


