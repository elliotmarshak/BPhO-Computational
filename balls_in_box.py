import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

g = 400
C = 0.9
fps = 60

class Ball:
    def __init__(self, x, y, r, m, colour):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.radius = r
        self.mass = m
        self.colour = colour
    
    def update(self, dt):
        self.vel.y += g * dt
        self.pos += self.vel * dt

        if self.pos.x < self.radius: #collision checks with walls
            self.pos.x = self.radius
            self.vel.x *= -C
        if self.pos.x > WIDTH - self.radius:
            self.pos.x = WIDTH - self.radius
            self.vel.x *= -C
        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.vel.y *= -C
        if self.pos.y > HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.vel.y *= -C
        
    def draw(self):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)

def ball_collision(ball1, ball2):
    delta = (ball2.pos - ball1.pos)
    dist = delta.length()
    if dist > ball1.radius + ball2.radius: #collisions are when the distance between the centres is less than the sum of the radii bc then they overlap
        return

    n = delta.normalize() #gives the unit vector pointing along the line of impact
    #only the velocities along this line so change so we turn a 2d problem into a 1d problem
    
    #projects the velocities onto this line
    u1 = ball1.vel.dot(n)
    u2 = ball2.vel.dot(n)

    #use the zero momentum frame maths from the BPhO Computational lecture
    v = (ball1.mass * u1 + ball2.mass * u2) / (ball1.mass + ball2.mass)

    v1n = -C * (u1-v) + v
    v2n = -C * (u2-v) + v
    ball1.vel += (v1n - u1) * n
    ball2.vel += (v2n - u2) * n

    overlap = ball1.radius + ball2.radius - dist
    # correction = n * (overlap / 2)
    # ball1.pos -= correction
    # ball2.pos += correction
    ball1.pos -= n * overlap * (ball2.mass / (ball1.mass + ball2.mass)) 
    ball2.pos += n * overlap * (ball1.mass / (ball1.mass + ball2.mass))
    #because this is in discrete time, the balls may overlap over eachother (which is how collisions are detected in the first place)
    #the commented code above does a poor job correcting for this and looks unrealistic
    #instead the correction factor (which is just the overlap in the direction of the collision line, so overlap * n) is scaled
    #in proportion to share of the total mass (lighter object should move more, heavier object moves less

ball1 = Ball(400, 100, 20, 1, (255, 0, 0))
ball2 = Ball(420, 50, 30, 3, (0, 255, 0))

while True:
    dt = clock.tick(fps)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    ball1.update(dt)
    ball2.update(dt)
    ball_collision(ball1, ball2)

    screen.fill((0,0,0))
    ball1.draw()
    ball2.draw()
    pygame.display.flip()

