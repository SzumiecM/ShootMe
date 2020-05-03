import pygame
import math
import sys

pygame.init()

screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("JPWP-project")
screen_CENTER = 600, 300

class Player(object):

    def __init__(self):
        self.x, self.y = screen_CENTER
        self.surface = pygame.image.load("player&hand.png")
        self.rotated_surface = self.surface.copy()
        self.rect = self.surface.get_rect()
        self.speed = 0.6

    def rotate(self, angle):
        self.rotated_surface = pygame.transform.rotate(self.surface, angle)
        self.rect = self.rotated_surface.get_rect(center=screen.get_rect().center)

    def draw(self):
        screen.blit(self.rotated_surface, self.rotated_surface.get_rect(center=(self.x, self.y)))

player1 = Player()

running = True

def redraw():
    screen.fill((0, 0, 0))
    player1.draw()
    pygame.display.flip()
    pygame.display.update()

while (running):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player1.x -= player1.speed
    if keys[pygame.K_d]:
        player1.x += player1.speed
    if keys[pygame.K_w]:
        player1.y -= player1.speed
    if keys[pygame.K_s]:
        player1.y += player1.speed

    elif e.type == pygame.MOUSEMOTION:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_x - player1.x, mouse_y - player1.y)
        angle = math.degrees(angle) + 180
        player1.rotate(angle)

    redraw()
pygame.quit()
