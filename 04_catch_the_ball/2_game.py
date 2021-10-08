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
balls = [] #массив координат шариков
N = 0 #количество очков

def new_ball():
    '''рисует новый шарик и возвращает его координаты'''
    global x, y, r
    x = randint(100, 800)
    y = randint(100, 500)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r

def mouse_xy(event):
    '''Возвращает координаты мыши'''
    X = event.pos[0]
    Y = event.pos[1]
    return X, Y


def check_click(xyr, xy):
    '''
    :param xyr: Тройка координат и радиуса шарика (x, y, r)
    :param xy: Пара координат мыши (x, y)
    :return: Возвращает True если попасть по шарику кликом и False если не попасть
    '''
    if (xy[0]-xyr[0])**2 + (xy[1]-xyr[1])**2 <= xyr[2]**2:
        return True
    else:
        return False

pygame.display.update()
clock = pygame.time.Clock()
finished = False


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(N)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(check_click(balls[len(balls)-1], mouse_xy(event)))
            #print(balls[len(balls)-1])
            #print(mouse_xy(event))
            for i in range(len(balls)):
                if check_click(balls[i], mouse_xy(event)):
                    N += 1
                    print(N)
    balls = []
    for i in range(5):
        balls.append(new_ball())
    pygame.display.update()
    screen.fill(BLACK)


pygame.quit()