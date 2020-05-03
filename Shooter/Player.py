from Instances import *


class Player(Obstacle):

    images = {}

    @staticmethod
    def add_image(name, image):
        Player.images[name] = image

    def __init__(self, gameplay, x, y, size, image):
        self.speed = 1
        self.zoom = 2
        self.weapon = None
        self.live = 100
        super(Player, self).__init__(gameplay, x, y, size, image)
        image = Player.images['player&hand']

    def move(self, direction, timedelta):
        #print(self.x, self.y)
        step = self.speed*timedelta
        if direction == 'up':
            self.y -= step
        elif direction == 'down':
            self.y += step
        elif direction == 'right':
            self.x += step
        elif direction == 'left':
            self.x -= step

        self.rect = self.image.get_rect().move(self.x, self.y)

    def set_weapon(self, weapon):
        self.weapon = weapon
        weapon.x = -1
        weapon.y = -1
