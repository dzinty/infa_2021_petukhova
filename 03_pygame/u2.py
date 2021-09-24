import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 400))

rect(screen, (255, 222, 173), (0, 0, 600, 85))
rect(screen, (255, 217, 196), (0, 85, 600, 85))
rect(screen, (255, 222, 173), (0, 170, 600, 85))
rect(screen, (184, 141, 170), (0, 250, 600, 150))
circle(screen, (255, 255, 0), (300, 100), 40)
#polygon(screen, (178, 34, 34), [(50 + x/20, 100+(-15+x/100)**2/2) for x in range(0, 3000)], 0)

polygon(screen, (178, 34, 34), [(0, 270), (0, 200), (110, 255), (130, 210), (175, 235), (190, 180), (245, 195),
                                (290, 225), (395, 215), (490, 210), (515, 180), (540, 200), (555, 165), (570, 170),
                                (600, 140), (600, 260)], 0)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
