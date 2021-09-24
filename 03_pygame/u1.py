import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (255, 255, 255), (50, 50, 300, 300))
#polygon(screen, (0, 0, 255), [(100,100), (200,50),(300,100), (100,100)], 5)
circle(screen, (255, 215, 0), (200, 200), 100)
circle(screen, (255, 0, 0), (160, 180), 20)
circle(screen, (255, 0, 0), (240, 180), 15)
circle(screen, (0, 0, 0), (160, 180), 10)
circle(screen, (0, 0, 0), (240, 180), 6)
rect(screen, (0, 0, 0), (150, 250, 100, 10), )
polygon(screen, (0, 0, 0), [(200, 51), (195, 125),(205,125)])
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
