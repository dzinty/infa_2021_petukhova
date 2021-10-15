import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
X_SIZE = 900
Y_SIZE = 600
screen = pygame.display.set_mode((X_SIZE, Y_SIZE))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
balls = [] #массив параметров шариков
N = 0 #количество очков

def new_ball():
    '''рисует новый шарик и возвращает его координаты и цвет'''
    x = randint(100, X_SIZE-100)
    y = randint(100, Y_SIZE-100)
    r = randint(10, 100)
    Vx = randint(-10, 10)
    Vy = randint(-10, 10)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return [x, y, r], color, [Vx, Vy]

def mouse_xy(event):
    '''Возвращает координаты мыши'''
    X = event.pos[0]
    Y = event.pos[1]
    return X, Y

def draw_ball(params):
    '''
    Рисует шарик по его параметрам (цвет, x, y, r)
    '''
    color = params[1]
    (X, Y) = (params[0][0], params[0][1])
    r = params[0][2]
    circle(screen, color, (X, Y), r)

def move_ball(params, i):
    '''Двигает шарики'''
    (X, Y) = (params[0][0], params[0][1])
    (Vx, Vy) = (params[2][0], params[2][1])
    r = params[0][2]
    X += Vx
    Y += Vy

    if X>X_SIZE-r or X<r:
        Vx = -Vx

    if Y>Y_SIZE-r or Y<r:
        Vy = -Vy

    balls[i][0][0] = X
    balls[i][0][1] = Y
    balls[i][2][0] = Vx
    balls[i][2][1] = Vy


def check_click_ball(xyr, xy):
    '''
    :param xyr: Тройка координат и радиуса шарика (x, y, r)
    :param xy: Пара координат мыши (x, y)
    :return: Возвращает True если попасть по шарику кликом и False если не попасть
    '''
    if (xy[0]-xyr[0])**2 + (xy[1]-xyr[1])**2 <= xyr[2]**2:
        return True
    else:
        return False

def new_square():
    '''Создает новый квадрат и сохраняет его координатыцвет и размер
    x,y - координаты центра квадрата
    r - длина стороны
    '''
    x = randint(100, X_SIZE-100)
    y = randint(100, Y_SIZE-100)
    r = randint(50, 100)
    color = COLORS[randint(0, 5)]
    return color, x, y, r

def draw_square(x, y, r, color):
    '''
    Рисует квадрат и его отражения
    :param x: координата центра квадрата по x
    :param y: координата центра квадрата по y
    :param r: длина стороны квадрата
    :param color: цвет квадрата в формате (R, G, B)
    :return:
    '''
    rect(screen, color, (x - r / 2, y - r / 2, r, r))
    rect(screen, color, (X_SIZE - x - r / 2, y - r / 2, r, r))
    rect(screen, color, (x - r / 2, Y_SIZE - y + r / 2, r, r))
    rect(screen, color, (X_SIZE - x - r / 2, Y_SIZE - y + r / 2, r, r))

def check_click_square(x, y, r, xy):
    '''

    :param x: координата центра квадрата по x
    :param y: координата центра квадрата по y
    :param r: длина стороны квадрата
    :param xy: Пара координат мыши (x, y)
    :return:
    '''
    if (xy[0]>x-r/2) and (xy[0]<x+r/2) and (xy[1]<y+r/2) and (xy[1]>y-r/2):
        return True
    else:
        return False


pygame.display.update()
clock = pygame.time.Clock()
finished = False

time = 0
game_time = 1000

alive = True
color, x, y, r = new_square()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print(N)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            i = 0
            while i < len(balls):
                if check_click_ball(balls[i][0], mouse_xy(event)):
                    N += 1
                    print(N)
                    balls.pop(i)
                i += 1
            if check_click_square(x, y, r, mouse_xy(event)):
                N += 5
                print(N)
                alive = False

    if len(balls) < 10:
        balls.append(new_ball())

    if alive:
        r -= 2
    else:
        color, x, y, r = new_square()
        alive = True
    if r<=0:
        alive = False

    draw_square(x, y, r, color)
    pygame.display.update()
    screen.fill(BLACK)
    for i in range(len(balls)):
        move_ball(balls[i], i)
        draw_ball(balls[i])
    time += 1
    if time > game_time:
        finished = True
        print('Total score:', N)


pygame.quit()