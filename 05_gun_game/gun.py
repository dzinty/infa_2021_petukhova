import math
from random import choice
from random import randint
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600




class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 100

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        g = 0.7
        k = 0.02
        self.x += self.vx
        self.y -= self.vy
        self.vx -= k * self.vx
        if (self.y >= HEIGHT-self.r - 1) or (self.y <= 10): self.vy = -self.vy
        else:
            self.vy -= g
            self.vy -= k * self.vy
        if (self.x >= WIDTH-self.r - 1) or (self.x <= 10): self.vx = -self.vx
        self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x-obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 200
        self.y = 450
        self.width = 5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, x=self.x, y=self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        x2 = self.x - self.width*math.sin(self.an)
        y2 = self.y + self.width*math.cos(self.an)
        x1 = self.x + math.cos(self.an)*self.f2_power
        y1 = self.y + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(self.screen, self.color,((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))


    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        vx = self.vx = randint(-10, 10)
        vy = self.vy = randint(-10,  10)
        r = self.r = randint(10, 50)
        self.live = 1
        color = self.color = choice(GAME_COLORS)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):

        self.x += self.vx
        self.y -= self.vy
        if (self.y >= HEIGHT-self.r - 1) or (self.y <= 10): self.vy = -self.vy
        if (self.x >= WIDTH-self.r - 1) or (self.x <= 10): self.vx = -self.vx

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
f1 = pygame.font.Font(None, 36)
bullet = 0
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(screen)
for i in range(2):
    targets.append(Target())
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        if b.live<0: balls.remove(b)
        b.draw()

    score = 0
    for target in targets:
        score += target.points
    text1 = f1.render('Score: ' + str(score), True, (0, 0, 0))
    screen.blit(text1, (10, 50))
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    for target in targets:
        target.move()
    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()

    gun.power_up()

pygame.quit()
