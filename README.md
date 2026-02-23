# BPhO-Computational
A collection of projects for simulating various physics problems from the British Physics Olympiad Computational
 ## Random Walk
 This was the first project from the introduction lecture. Here I simply use Matplotlib to graph randomly generated random walks (picks random direction and takes a step forward)

 ## Bouncing Ball
 From the second lecture (Kinematics). This models a simple ball moving up and down by using a coefficient of restitution.

 ## Balls in a Box
 Also from the second lecture, this one took a bit more work. The collisions now occur in 2D and 2 balls of different masses are dropped from slightly different locations and are allowed to bounce around the box, with acceleration due to gravity acting on them, as well as a fixed coefficient of restitution. The 2D collisions are easily broken down into a 1D problem along a collision axis by using the dot product to project the velocities onto this axis. Then, the Zero Momentum Frame is used to easily calculate the velocities after the collision. Some correction logic is also needed to deal with the errors of ball overlap caused by discrete time.
![balls_in_box](https://github.com/user-attachments/assets/d695729c-ca4d-4b91-b27f-944a7480b4d2)
