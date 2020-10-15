import pygame
import math
import random
pygame.init()

win = pygame.display.set_mode((1200, 700))

pygame.display.set_caption("Kaktus Bob")


class Player(object):
    def __init__(self, x, y, velx, vely, vel, height, width):
        self.vely = vely
        self.velx = velx
        self.y = y
        self.x = x
        self.vel = vel
        self.height = height
        self.width = width
    def move(self):
            self.x += self.velx
            self.y += self.vely


class Baloon(object):
    def __init__(self, x, y, velx, vely, vel, r, a):
        self.velx = velx
        self.vely = vely
        self.y = y
        self.x = x
        self.vel = vel
        self.r = r
        self.a = a
    def move(self):
        self.x += self.velx
        self.y += self.vely

class Projectile(object):
    def __init__(self, x0, y0, x1, y1, x, y, velx, vely, vel, r):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.vel = vel
        self.r = r
    def move(self):
        self.x += self.velx
        self.y += self.vely


def direction_x(Bob, x, y, vel):
    x = abs(Bob.x) - abs(x)
    y = abs(Bob.y) - abs(y)
    z = math.sqrt(x * x + y * y)
    if z == 0:
        z = 1
    nepoznata = (x * vel) // z
    return int(nepoznata)


def direction_y(Bob, x, y, vel):
    x = abs(Bob.x) - abs(x)
    y = abs(Bob.y) - abs(y)
    z = math.sqrt(x * x + y * y)
    nepoznata = (y * vel) // z
    return int(nepoznata)


def collision_ball_ball(Ball1, Ball2):
    if (Ball1.x - Ball2.x) * (Ball1.x - Ball2.x) + (Ball1.y - Ball2.y) * (Ball1.y - Ball2.y) <= (Ball1.r + Ball2.r) * (Ball1.r + Ball2.r):
        return True
    else:
        return False


Bob = Player(600, 350, 0, 0, 10, 40, 30)
Alfa = Baloon(0, 0, 0, 0, 5, 30, 1)

baloons = []
timer = 100
limit = 100
counter = 1
timer_projectile = 0
limit_projectile = 100
vel_projectile = 30
safe_switch = False


run = True
while run:
    win.fill((0, 0, 0))

    pygame.time.delay(15)

    timer += counter
    timer_projectile += 1
    mouse_click = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    fence_distance = 50

    key = pygame.key.get_pressed()
    if key[pygame.K_w] and Bob.y > 0 + fence_distance:
        Bob.vely -= Bob.vel
    if key[pygame.K_s] and Bob.y < 700 - Bob.height - fence_distance:
        Bob.vely += Bob.vel
    if key[pygame.K_a] and Bob.x > 0 + fence_distance:
        Bob.velx -= Bob.vel
    if key[pygame.K_d] and Bob.x < 1200 - Bob.width - fence_distance:
        Bob.velx += Bob.vel
    if Bob.velx != 0 and Bob.vely != 0:
        Bob.velx = (Bob.velx * 2) // 3
        Bob.vely = (Bob.vely * 2) // 3
    Bob.move()
    Bob.velx = 0
    Bob.vely = 0


    if timer >= limit:
        strana = random.randint(0, 4)
        if strana == 1:
            x = random.randint(0, 1200)
            y = -Alfa.r
        elif strana == 2:
            y = random.randint(0, 900)
            x = -Alfa.r
        elif strana == 3:
            x = random.randint(0, 1200)
            y = 900 + Alfa.r
        else:
            y = random.randint(0, 900)
            x = 1200 + Alfa.r
        vel_x = direction_x(Bob, x, y, Alfa.vel)
        vel_y = direction_y(Bob, x, y, Alfa.vel)
        baloons.append(Baloon(x, y, vel_x, vel_y, Alfa.vel, Alfa.r, Alfa.a))
        timer = 0


    if mouse_click and timer_projectile >= limit_projectile:
        position = pygame.mouse.get_pos()
        Mouse = Player(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, 0, 0, 0)
        Wind = Projectile(position[0], position[1],
                            Bob.x, Bob.y, Bob.x, Bob.y, direction_x(Mouse, Bob.x,
                            Bob.y, vel_projectile), direction_y(Mouse, Bob.x, Bob.y,
                            vel_projectile), vel_projectile, 50)
        safe_switch = True
        timer_projectile = 0

    if safe_switch:
        Wind.r += 4
        Wind.move()
        pygame.draw.circle(win, (110, 110, 110), (Wind.x, Wind.y), Wind.r)


    for i in range(0, len(baloons)):
        velx = direction_x(Bob, baloons[i].x, baloons[i].y, Alfa.vel)
        vely = direction_y(Bob, baloons[i].x, baloons[i].y, Alfa.vel)
        if baloons[i].velx <= velx - Alfa.a // 2:
            baloons[i].velx += Alfa.a
        elif baloons[i].velx >= velx + Alfa.a // 2:
            baloons[i].velx -= Alfa.a
        if baloons[i].vely <= vely - Alfa.a // 2:
            baloons[i].vely += Alfa.a
        elif baloons[i].vely >= vely + Alfa.a // 2:
            baloons[i].vely -= Alfa.a

        if safe_switch:
             if collision_ball_ball(baloons[i], Wind):
                baloons[i].velx = -direction_x(Wind, baloons[i].x, baloons[i].y, 10)
                baloons[j].velx = -direction_x(Wind, baloons[i].x, baloons[i].y, 10)
                baloons[j].vely = -direction_y(Wind, baloons[i].x, baloons[i].y, 10) # ODBIJANJE BALONA O  VETAR
                baloons[i].vely = -direction_y(Wind, baloons[i].x, baloons[i].y, 30)

        baloons[i].move()

        for j in range (0, len(baloons)):
    #         pygame.draw.circle(win, (254, 254, 254), (baloons[i].x, baloons[i].y), Alfa.r, 0)
    #         if (baloons[i].x * baloons[i].x - Bob.x * Bob.x) * (baloons[i].x * baloons[i].x - Bob.x * Bob.x) + (baloons[i].y * baloons[i].y - Bob.y * Bob.y) * (baloons[i].y * baloons[i].y - Bob.y * Bob.y) <= (Alfa.r + Bob.width / 2) * (Alfa.r + Bob.width / 2):
    #             pygame.draw.rect(win, (255, 255, 255), (0, 0, 2000, 2000))
    #             pygame.display.update()
    #
            if collision_ball_ball(baloons[i], baloons[j]) and i != j:
                baloons[i].velx = -direction_x(baloons[j], baloons[i].x, baloons[i].y, 10)    # ODBIJANJE BALONA O BALON
                baloons[i].vely = -direction_y(baloons[j], baloons[i].x, baloons[i].y, 10)
            #pygame.time.delay(1)
            break


    # for i in range(len(baloons)):
    #     if (not baloons[i].x < -2 * Alfa.r 
    #             Bob.x = 600
    #             Bob.y = 350
    #             del baloons[:]and baloons[i].x > 1200 + 2 * Alfa.r) or (baloons[i].x < -2 * Alfa.r and not baloons[i].x > 2 * 1200 + Alfa.r):
    #         baloons.pop(i)
    #
    #     elif (not baloons[i].y < -2 * Alfa.r and baloons[i].y > 900 + 2 * Alfa.r) or (baloons[i].y < -2 * Alfa.r and not baloons[i].y > 900 + 2 * Alfa.r):
    #         baloons.pop(i)

    for i in range (0, len(baloons)):
        pygame.draw.circle(win, (200, 0, 200), (baloons[i].x, baloons[i].y), baloons[i].r)

    pygame.draw.circle(win, (200, 0, 0),pygame.mouse.get_pos(), 5)
    pygame.mouse.set_visible(False)
    pygame.draw.rect(win, (200, 250, 100), (Bob.x, Bob.y, Bob.width, Bob.height))
    pygame.display.update()
pygame.quit()