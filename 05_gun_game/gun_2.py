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


class Laser:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса laser

        Args:
        x - начальное положение лазера по горизонтали
        y - начальное положение лазера по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.length = 20
        self.width = 5
        self.vx = 0
        self.vy = 0
        self.an = 1
        self.r = 3
        self.color = choice(GAME_COLORS)
        self.live = 500

    def move(self):
        """Переместить лазер по прошествии единицы времени.

        Метод описывает перемещение лазера за один кадр перерисовки.
        """
        self.x += self.vx
        self.y -= self.vy
        self.live -= 1

    def draw(self):
        x2 = self.x - self.width * math.sin(self.an)
        y2 = self.y + self.width * math.cos(self.an)
        x1 = self.x + math.cos(self.an) * self.length
        y1 = self.y + math.sin(self.an) * self.length
        x3 = x2 + math.cos(self.an) * self.length
        y3 = y2 + math.sin(self.an) * self.length
        pygame.draw.polygon(self.screen, self.color, ((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения лазера и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= obj.r ** 2:
            return True
        else:
            return False


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


class Bomb:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса bomb

        Args:
        x - положение бомбы по горизонтали
        y - положение бомбы по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 5
        self.color = BLACK

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 200
        self.y = 450
        self.vx = 0
        self.vy = 0
        self.width = 5
        self.health = 20

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, type = 1):
        """Выстрел снарядом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        global balls, lasers, bullet
        bullet += 1
        if type == 1:
            new_ball = Ball(self.screen, x=self.x, y=self.y)
            new_ball.r += 5
            self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.an)
            new_ball.vy = - self.f2_power * math.sin(self.an)
            balls.append(new_ball)
        if type == 2:
            new_laser = Laser(self.screen, x=self.x, y=self.y)
            self.an = math.atan2((event.pos[1] - new_laser.y), (event.pos[0] - new_laser.x))
            new_laser.an = self.an
            new_laser.vx = self.f2_power * math.cos(self.an)
            new_laser.vy = - self.f2_power * math.sin(self.an)
            new_laser.length = self.f2_power
            lasers.append(new_laser)
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
        pygame.draw.rect(self.screen, BLACK, (self.x-10, self.y-10, 20, 20))

        x0 = self.x + 0.5*self.width * math.sin(self.an)
        y0 = self.y - 0.5*self.width * math.cos(self.an)
        x2 = x0 - self.width*math.sin(self.an)
        y2 = y0 + self.width*math.cos(self.an)
        x1 = x0 + math.cos(self.an)*self.f2_power
        y1 = y0 + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(self.screen, self.color,((x0, y0), (x1, y1), (x3, y3), (x2, y2)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


    def move(self):
        if self.x < 10:
            self.vx = 0
            self.x = 10
        elif self.x > WIDTH-10:
            self.vx = 0
            self.x = WIDTH-10
        self.x += self.vx
        if self.y < 10:
            self.y = 10
            self.vy = 0
        elif self.y > HEIGHT - 10:
            self.y = HEIGHT-10
            self.vy = 0
        self.y += self.vy

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения пушки и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (5+obj.r) ** 2:
            return True
        else:
            return False

class Target:
    def __init__(self):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()
        self.timer = randint(50, 100)

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

class EnemyGun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.an = 1
        self.color = RED
        self.R = randint(100, 250)
        self.r = 5
        self.x = WIDTH/2
        self.y = HEIGHT/2 - self.R
        self.vx = 0
        self.vy = 0
        self.width = 5
        self.health = 20
        self.timer = 20
        self.v = 3
    def fire(self, obj, type = 1):
        """Выстрел снарядом.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения объекта.
        """
        global enemy_lasers
        new_laser = Laser(self.screen, x=self.x, y=self.y)
        self.an = math.atan2((obj.y - new_laser.y), (obj.x - new_laser.x))
        new_laser.an = self.an
        new_laser.vx = self.f2_power * math.cos(self.an)
        new_laser.vy = - self.f2_power * math.sin(self.an)
        new_laser.length = self.f2_power
        enemy_lasers.append(new_laser)
        self.f2_power = 10

    def targetting(self, obj):
        """Прицеливание. Зависит от положения объекта."""
        self.an = math.atan2((obj.y-self.y), (obj.x-self.x))

    def draw(self):
        pygame.draw.rect(self.screen, GREY, (self.x-10, self.y-10, 20, 20))

        x0 = self.x + 0.5*self.width * math.sin(self.an)
        y0 = self.y - 0.5*self.width * math.cos(self.an)
        x2 = x0 - self.width*math.sin(self.an)
        y2 = y0 + self.width*math.cos(self.an)
        x1 = x0 + math.cos(self.an)*self.f2_power
        y1 = y0 + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(self.screen, self.color,((x0, y0), (x1, y1), (x3, y3), (x2, y2)))


    def move(self):
        phi = math.atan2((-self.y+HEIGHT/2), (self.x - WIDTH/2))
        self.vx = self.v*math.sin(phi)
        self.vy = self.v*math.cos(phi)
        self.x += self.vx
        self.y += self.vy




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
f1 = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 100)
bullet = 0
balls = []
lasers = []
enemy_lasers = []
targets = []
bombs = []
enemies = []
score_0 = 0

clock = pygame.time.Clock()
gun = Gun(screen)
enemies.append(EnemyGun(screen))
for i in range(2):
    targets.append(Target())
finished = False
bullet_type = 1

while not finished:
    screen.fill(WHITE)
    gun.move()
    gun.draw()
    for enemy1 in enemies:
        enemy1.move()
        enemy1.targetting(gun)
        enemy1.draw()
        if enemy1.timer < 0:
            enemy1.fire(gun)
            enemy1.timer = 20
        enemy1.timer -= 1
        if enemy1.health < 0:
            enemies.remove(enemy1)
            enemies.append(EnemyGun(screen))
            score_0 += 100
    for bomb in bombs:
        bomb.draw()
    for target in targets:
        target.draw()
    for b in balls:
        if b.live<0: balls.remove(b)
        b.draw()
    for l in lasers:
        if l.live<0: lasers.remove(l)
        l.draw()
    for l in enemy_lasers:
        if l.live<0: enemy_lasers.remove(l)
        l.draw()

    score = score_0
    for target in targets:
        score += target.points
    text1 = f1.render('Score: ' + str(score), True, (0, 0, 0))
    text2 = f1.render('HP: ' + str(gun.health), True, (0, 0, 0))
    screen.blit(text1, (10, 50))
    screen.blit(text2, (10, 10))
    if gun.health <= 0:
        finished = True
        text = f2.render('GAME OVER', True, (183, 3, 3))
        screen.fill(BLACK)
        screen.blit(text, (200, 250))
        pygame.display.update()
        pygame.time.delay(2000)
    pygame.display.update()

    if score > 300:
        finished = True
        text = f2.render('YOU WIN', True, (102, 255, 3))
        screen.blit(text, (200, 250))
        pygame.display.update()
        pygame.time.delay(2000)


    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.KEYUP:
            if (not pygame.key.get_pressed()[pygame.K_d]) and (not pygame.key.get_pressed()[pygame.K_a]):
                gun.vx = 0
            if (not pygame.key.get_pressed()[pygame.K_w]) and (not pygame.key.get_pressed()[pygame.K_s]):
                gun.vy = 0
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_d]:
                gun.vx = 5
            elif pygame.key.get_pressed()[pygame.K_a]:
                gun.vx = -5
            if pygame.key.get_pressed()[pygame.K_w]:
                gun.vy = -5
            elif pygame.key.get_pressed()[pygame.K_s]:
                gun.vy = 5


        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_1]:
                bullet_type = 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_2]:
                bullet_type = 2

        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, type = bullet_type)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for target in targets:
        if target.timer <= 0:
            bombs.append(Bomb(screen, target.x, target.y))
            target.timer = randint(50, 100)
        target.timer -= 1
        target.move()

    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
        for enemy in enemies:
            if b.hittest(enemy):
                enemy.health -= 1



    for l in lasers:
        l.move()
        for target in targets:
            if l.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
        for enemy in enemies:
            if l.hittest(enemy):
                enemy.health -= 1


    for l in enemy_lasers:
        l.move()
        if gun.hittest(l):
            enemy_lasers.remove(l)
            gun.health -= 1

    for b in bombs:
        if gun.hittest(b):
            bombs.remove(b)
            gun.health -= 1

    gun.power_up()




pygame.quit()
