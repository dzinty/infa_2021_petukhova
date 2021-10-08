import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 2
screen = pygame.display.set_mode((900, 600))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    '''рисует новый шарик '''
    global x, y, r
    x = randint(100, 800)
    y = randint(100, 500)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r


def click(event):
    '''возвращает координаты круга, существующего на момент клика мышкой'''
    return x, y, r


def mouse_xy(event):
    '''Возвращает координаты мыши'''
    X = event.pos[0]
    Y = event.pos[1]
    return X, Y


def check_click(event, xy):
    '''
    :param event:
    :param xy: Пара координат мыши (x, y)
    :return: Возвращает True если попасть по шарику кликом и False если не попасть
    '''
    if (xy[0]-x)**2+(xy[1]-y)**2 <= r**2:
        return True
    else:
        return False

pygame.display.update()
clock = pygame.time.Clock()
finished = False
N = 0 #количество очков

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(N)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            click(event)
            print(check_click(event, mouse_xy(event)))
            print(event.pos)
            if(check_click(event, mouse_xy(event))):
                N += 1
                print(N)
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()