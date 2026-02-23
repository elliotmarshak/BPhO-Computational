import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fps = 60
radius = 20
max_bounces = 50
g = 9.81
c = 0.8 #coefficient of restitution
height = 5

x = height
v = 0
bounces = 0

while bounces < max_bounces:

    dt = clock.tick(fps)/1000 #clock.tick returns ms

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pass

    x = x - v*dt - 0.5 * g * (dt)**2 #We are taking downwards as positive
    v = v + g*dt
    if x < 0 and v > 0: #means there is a bounce
        bounces += 1
        v = -c*v


    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (WIDTH//2, HEIGHT-radius-(x/height*HEIGHT)), radius)
    pygame.display.flip()


pygame.quit()