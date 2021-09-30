import pygame
from pygame.draw import *
from random import random
import math

X_size = 1200
Y_size = 600


def mountain_generator(delta, x_size, y_size):
    points = []
    x = 0
    y = 0
    sign = 1
    while x < x_size:
        points.append((x, max(1, y)))
        x += random()*delta
        y += sign * random() * delta
        if y > random()*y_size:
            sign = -sign
        if y < 0: sign = 1
        if y > y_size: y = y_size
    points.append((x_size,0))
    return points


def bird_generator(size):
    x = [0.1*j for j in range(-40, 41)]
    points = []
    for j in range(len(x)):
       points.append((size * x[j], size * math.sqrt(math.fabs(x[j]))))
    for j in range(len(x)):
       points.append((size * x[::-1][j], size * (0.75 * math.sqrt(math.fabs(x[::-1][j])) + 0.5)))
    return points


pygame.init()

FPS = 30
screen = pygame.display.set_mode((X_size, Y_size))
r_sun = Y_size/10
rect(screen, (254, 214, 163), (0, 0, X_size, 0.225*Y_size))
rect(screen, (254, 214, 197), (0, 0.225*Y_size, X_size, 0.225*Y_size))
rect(screen, (254, 214, 163), (0, 0.45*Y_size, X_size, 0.225*Y_size))
rect(screen, (180, 135, 149), (0, 0.675*Y_size, X_size, 0.325*Y_size))
circle(screen, (252, 239, 27), (X_size/2, Y_size/4), r_sun)

polygon(screen, (252, 153, 45), [(x, 0.45*Y_size-y) for (x, y) in mountain_generator(10, X_size/2-r_sun-10, Y_size/4)], 0)
polygon(screen, (252, 153, 45), [(x+X_size/2-r_sun-10, 0.45*Y_size-y) for (x, y) in mountain_generator(10, 2*(r_sun+10), 0.2*Y_size-r_sun-10)], 0)
polygon(screen, (252, 153, 45), [(x+X_size/2+r_sun+10, 0.45*Y_size-y) for (x, y) in mountain_generator(10, X_size/2-r_sun-10, Y_size/4)], 0)

polygon(screen, (173, 65, 49), [(x, 0.7*Y_size-y) for (x, y) in mountain_generator(20, X_size, Y_size/2)], 0)

polygon(screen, (44, 7, 33), [(x, Y_size-y) for (x, y) in mountain_generator(100, X_size/3, Y_size)], 0)
polygon(screen, (44, 7, 33), [(X_size/3+x, Y_size-y) for (x, y) in mountain_generator(50, X_size/3, Y_size/4)], 0)
polygon(screen, (44, 7, 33), [(X_size/3*2+x, Y_size-y) for (x, y) in mountain_generator(100, X_size/3, Y_size)], 0)

num_birds = 9
for i in range(num_birds):
    x0 = random() * X_size
    y0 = random() * (Y_size-100)
    size = random()*Y_size/40
    polygon(screen, (64, 27, 3), [(x0+x, y0-y) for (x, y) in bird_generator(size)], 0)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
