# BPhO-Computational
A collection of projects for simulating various physics problems from the British Physics Olympiad Computational
 ## Random Walk
 This was the first project from the introduction lecture. Here I simply use Matplotlib to graph randomly generated random walks (picks random direction and takes a step forward)

 ## Bouncing Ball
 From the second lecture (Kinematics). This models a simple ball moving up and down by using a coefficient of restitution.

 ## Balls in a Box
 Also from the second lecture, this one took a bit more work. The collisions now occur in 2D and 2 balls of different masses are dropped from slightly different locations and are allowed to bounce around the box, with acceleration due to gravity acting on them, as well as a fixed coefficient of restitution. The 2D collisions are easily broken down into a 1D problem along a collision axis by using the dot product to project the velocities onto this axis. Then, the Zero Momentum Frame is used to easily calculate the velocities after the collision. Some correction logic is also needed to deal with the errors of ball overlap caused by discrete time.
![balls_in_box](https://github.com/user-attachments/assets/d695729c-ca4d-4b91-b27f-944a7480b4d2)

## Orbits (Gravity and Astrophysics)
This was from the Gravity and Astrophysics lecture. First I made a simple circular orbit of a planet orbitting a central body. I just used a simple uniform rate of change of angle and found the position using trigonometry. For the elliptical orbits, I used 3 different methods to calculate the positions with respect to time. First I used the Verlet Method to assume constant acceleration between discrete time steps. For the second one, I used the Runge-Kutta method to calculate the position. Finally I used the Newton-Raphson method to solve the Kepler equation to find the eccentric anomaly. Then the true anomaly (theta) can be found and the position can be calculated using the elliptic formula for r in terms of theta.
