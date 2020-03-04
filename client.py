import pygame

window = pygame.display.set_mode((600,600))
pygame.display.set_caption('Client')


class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.movedist = 10

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, 20, 20))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.movedist
        if keys[pygame.K_a]:
            self.x -= self.movedist
        if keys[pygame.K_s]:
            self.y += self.movedist
        if keys[pygame.K_d]:
            self.x += self.movedist

def refresh(window, player):
    window.fill((0, 0, 0))
    player.draw(window)
    pygame.display.update()

run = True
p = Player(300, 300, (255, 0, 0))
clock = pygame.time.Clock()

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    p.move()
    refresh(window, p)