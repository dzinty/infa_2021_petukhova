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


class Laser():
    def __init__(self, x, y):
        """ Конструктор класса laser

        Args:
        x - начальное положение лазера по горизонтали
        y - начальное положение лазера по вертикали
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 100
        self.length = 20
        self.width = 5
        self.an = 1
        self.r = 3

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
        pygame.draw.polygon(screen, self.color, ((self.x, self.y), (x1, y1), (x3, y3), (x2, y2)))

class Ball(Laser):
    def __init__(self, x, y):
        Laser.__init__(self, x, y)
        self.r = 15
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
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Bomb:
    def __init__(self, x, y):
        """ Конструктор класса bomb

        Args:
        x - положение бомбы по горизонтали
        y - положение бомбы по вертикали
        """
        self.x = x
        self.y = y
        self.r = 5
        self.color = BLACK

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.base_color = BLACK
        self.x = 200
        self.y = 450
        self.vx = 0
        self.vy = 0
        self.width = 5
        self.health = 20
        self.type = 1

    def mouse_xy(self, event):
        """
        Принимает событие, возвращает кортеж координат его положения
        :param event:
        :return:
        """
        x = event.pos[0]
        y = event.pos[1]
        return x, y

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, xy):
        """Выстрел снарядом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости снаряда vx и vy зависят от положения мыши.
        """
        if self.type == 1:
            new_bullet = Ball(x=self.x, y=self.y)
        else:
            new_bullet = Laser(x=self.x, y=self.y)

        self.an = math.atan2((xy[1] - new_bullet.y), (xy[0] - new_bullet.x))
        new_bullet.an = self.an
        new_bullet.vx = self.f2_power * math.cos(self.an)
        new_bullet.vy = - self.f2_power * math.sin(self.an)
        new_bullet.length = self.f2_power
        self.f2_on = 0
        self.f2_power = 10
        return new_bullet

    def targetting(self, xy):
        """Прицеливание. Зависит от положения мыши."""
        self.an = math.atan2((xy[1]-self.y), (xy[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.rect(screen, self.base_color, (self.x-10, self.y-10, 20, 20))
        x0 = self.x + 0.5*self.width * math.sin(self.an)
        y0 = self.y - 0.5*self.width * math.cos(self.an)
        x2 = x0 - self.width*math.sin(self.an)
        y2 = y0 + self.width*math.cos(self.an)
        x1 = x0 + math.cos(self.an)*self.f2_power
        y1 = y0 + math.sin(self.an)*self.f2_power
        x3 = x2 + math.cos(self.an) * self.f2_power
        y3 = y2 + math.sin(self.an) * self.f2_power
        pygame.draw.polygon(screen, self.color,((x0, y0), (x1, y1), (x3, y3), (x2, y2)))

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

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения пушки и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r+obj.r) ** 2:
            return True
        else:
            return False

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if (self.y >= HEIGHT-self.r - 1) or (self.y <= 10): self.vy = -self.vy
        if (self.x >= WIDTH-self.r - 1) or (self.x <= 10): self.vx = -self.vx

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.r, 1)


class EnemyGun(Gun):
    def __init__(self):
        Gun.__init__(self)
        self.base_color = (50, 255, 0)
        self.R = randint(100, 250)
        self.x = WIDTH/2
        self.y = HEIGHT/2 - self.R
        self.timer = 20
        self.v = 3
        self.type = 2

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
bullets = []
enemy_lasers = []
targets = []
bombs = []
enemies = []
score_0 = 0

clock = pygame.time.Clock()
gun = Gun()
enemies.append(EnemyGun())
for i in range(2):
    targets.append(Target())
finished = False


while not finished:
    screen.fill(WHITE)
    gun.move()
    gun.draw()

    for enemy in enemies:
        enemy.move()
        enemy.targetting((gun.x, gun.y))
        enemy.draw()
        if enemy.timer < 0:
            enemy_lasers.append(enemy.fire2_end((gun.x, gun.y)))
            enemy.timer = 20
        enemy.timer -= 1
        if enemy.health < 0:
            enemies.remove(enemy)
            enemies.append(EnemyGun())
            enemies.append(EnemyGun())
            score_0 += 100

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
                gun.type = 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_2]:
                gun.type = 2

        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            bullets.append(gun.fire2_end(gun.mouse_xy(event)))
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(gun.mouse_xy(event))

    for target in targets:
        target.draw()
        target.move()
        if target.timer <= 0:
            bombs.append(Bomb(target.x, target.y))
            target.timer = randint(50, 100)
        target.timer -= 1


    for b in bullets:
        if b.live < 0: bullets.remove(b)
        b.draw()
        b.move()
        for target in targets:
            if target.hittest(b) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
        for enemy in enemies:
            if enemy.hittest(b):
                enemy.health -= 1

    for l in enemy_lasers:
        if l.live < 0: enemy_lasers.remove(l)
        l.draw()
        l.move()
        if gun.hittest(l):
            enemy_lasers.remove(l)
            gun.health -= 1

    for bomb in bombs:
        bomb.draw()
        if gun.hittest(bomb):
            bombs.remove(bomb)
            gun.health -= 1
            
    pygame.display.update()
    gun.power_up()

pygame.quit()
