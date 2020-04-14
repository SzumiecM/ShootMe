import pygame
#Everything that can be visible as an object in the game
import Gameplay
class Instance:

    angle = 0

    def __init__(self, gameplay, x, y, size, image):
        self.gameplay = gameplay
        self.size = size
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect().move(self.x, self.y) if image is not None else None
        # Default position of an image

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


    #abstract method, to get visibility area
    #to check if it is visible on the screen
    def get_visibility_range(self):
        return self.rect

    # abstract method, to get area that object takes on the map
    def get_area(self):
        return self.size * self.size

    def get_image(self):
        return self.image



class Obstacle(Instance):

    # abstract method, to get collider
    # it indicates where players cannot move
    # Default value is the same as its visibility
    def get_collider(self):
        return self.rect

    def get_width(self):
        return self.rect.w

    def get_height(self):
        return self.rect.h

    def get_damge(self, amount):
        self.size -= amount
        if self.size < self.gameplay.min_obstacle_size:
            self.gameplay.drop(self)
        else:
            self.image = self.gameplay.scale_image(self.image, self.size)
            self.rect = self.image.get_rect().move(self.x, self.y) if self.image is not None else None



class Rock(Obstacle):

    def get_area(self):
        return self.size * self.size * 3.14

    '''
        def get_visibility_range(self):
            return self.image.get_rect().move(self.x - self.size//2, self.y - self.size//2)

        def get_collider(self):
            return self.image.get_rect()
    '''

class Weapon(Instance):

    def __init__(self,gameplay, type, image):
        self.type = type
        if type == "gun":
            self.fire_rate = 10
            self.recoil_time = 30
            self.max_ammo = 30
            self.distance = 100
            self.damage = 20
        elif type == "shotgun":
            self.fire_rate = 10
            self.recoil_time = 30
            self.max_ammo = 30
            self.distance = 100
            self.damage = 20
        elif type == "thompson":
            self.fire_rate = 10
            self.recoil_time = 30
            self.max_ammo = 30
            self.distance = 100
            self.damage = 20
        else: #hand
            self.fire_rate = 1
            self.recoil_time = 0
            self.max_ammo = -1
            self.distance = 40
            self.damage = 2

        super(Weapon, self).__init__(gameplay, -1, -1, 0, image)

