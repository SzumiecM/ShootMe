import pygame

class Bullet:
    def __init__(self, x, y, rad, color):
        self.x = x
        self.y = y
        self.color = color
        self.pos = (x, y)
        self.radius = rad
        self.vel = 10

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]: self.x -= self.vel
        if keys[pygame.K_d]: self.x += self.vel
        if keys[pygame.K_w]: self.y -= self.vel
        if keys[pygame.K_s]: self.y += self.vel

        self.update()

    def update(self):
        self.pos = (self.x, self.y)