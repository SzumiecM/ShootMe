import pygame
import math
import sys
import settings
pygame.init()

screen = pygame.display.set_mode(settings.screen_SIZE)
pygame.display.set_caption(settings.screen_TITLE)
running = True

class Player(object):

    def __init__(self):
        self.x, self.y = settings.screen_CENTER
        self.surface = pygame.image.load('C:/Users/majka/OneDrive/Pulpit/PythonProjekty/Game/pic2.png')
        self.rotated_surface = self.surface.copy()
        self.rect = self.surface.get_rect()
        self.speed = 0.1
        self.w = 64
        self.h = 64

    def rotate(self, angle):
        rot_image = pygame.transform.rotozoom(self.surface, angle, 1)
        rot_rect = self.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.rotated_surface = rot_image


    def draw(self):
        screen.blit(self.rotated_surface, (self.x, self.y))


class projectile(object):

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
player1 = Player()
player2 = Player()

def redraw():
    screen.fill((0, 0, 0))
    player1.draw()
    for bullet in bullets:
        bullet.draw(screen)
    player2.draw()
    pygame.display.flip()
    pygame.display.update()


bullets = []
while (running):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                sys.exit()
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player1.x -= player1.speed
    if keys[pygame.K_d]:
        player1.x += player1.speed
    if keys[pygame.K_w]:
        player1.y -= player1.speed
    if keys[pygame.K_s]:
        player1.y += player1.speed
    if e.type == pygame.MOUSEBUTTONUP:
        if len(bullets) < 2:
            bullets.append(projectile(round(player1.x + player1.w // 2), round(player1.y + player1.h // 2), 6, (255, 10, 10)))

    elif e.type == pygame.MOUSEMOTION:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]
            angle = math.atan2(mouse_x - player1.x, mouse_y - player1.y)
            angle = angle * (180 / math.pi)
            player1.rotate(angle)

    if keys[pygame.K_LEFT]:
        player2.x -= player2.speed
    if keys[pygame.K_RIGHT]:
        player2.x += player2.speed
    if keys[pygame.K_UP]:
        player2.y -= player2.speed
    if keys[pygame.K_DOWN]:
        player2.y += player2.speed

    redraw()
pygame.quit()

