#Everything that can be visible as an object in the game
import math
import pygame
class Instance:
    angle = 0

    def __init__(self, gameplay, x, y, size, image):
        self.gameplay = gameplay
        self.size = size
        self.life = size
        self.x = float(x)
        self.y = float(y)
        self.speed = 0.0 #By default instances shouldn't move
        self.original_image = image
        self.image = gameplay.scale_image(image, size) if image is not None else None
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
        return self.image if self.image is not None else pygame.Surface((self.size, self.size))

    def move(self, direction, timedelta, step=0):
        step = self.speed * timedelta if step == 0 else step
        if direction == 'up':
            self.y -= step
        elif direction == 'down':
            self.y += step
        elif direction == 'right':
            self.x += step
        elif direction == 'left':
            self.x -= step

        self.adjust_collider()

    def adjust_collider(self):
        self.rect = self.image.get_rect().move(self.x, self.y)


class Pick_up(Instance):
    def __init__(self, gameplay, x, y, size, image, name):
        self.name = name
        super(Pick_up, self).__init__(gameplay, x, y, size, image)


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

    def get_damage(self, amount):
        self.life -= amount

        if not isinstance(self, Player):
            self.size -= amount
            self.x += amount * 3
            self.y += amount * 3

        if self.size < self.gameplay.min_obstacle_size*0.7 or self.life <= 0:
            self.gameplay.drop(self)
        elif not isinstance(self, Player):
            self.image = self.gameplay.scale_image(self.original_image, self.size)
            self.rect = self.image.get_rect().move(self.x, self.y) if self.image is not None else None


class Rock(Obstacle):

    def get_area(self):
        return self.size * self.size * 3.14


class Player(Obstacle):

    images = {}

    @staticmethod
    def add_image(name, image):
        Player.images[name] = image

    def __init__(self, gameplay, x, y, size, image):
        image = Player.images['player&hand']
        super(Player, self).__init__(gameplay, x, y, size, image)
        self.speed = 1
        self.zoom = 2
        self.weapon = None
        self.life = 100.0

    def set_weapon(self, weapon):
        self.weapon = weapon
        self.image = Player.images['player&' + weapon.type]
        weapon.x = -1
        weapon.y = -1

    def change_weapon_sprite(self, weapon_name):
        self.image = Player.images['player&' + weapon_name]

    def shot(self, image=None):
        x = self.x + 0.5 * self.size
        y = self.y + 0.5 * self.size
        bullet, num = self.weapon.shot(x, y, self.angle, image)
        if num == 0:
            self.set_weapon(Weapon(self.gameplay, 'hand', None))
        if bullet is not None:
            bullet.set_owner(self)
        return bullet


class Bullet(Obstacle):
    def __init__(self, gameplay, x, y, size, image, angle, speed, damage, distance):
        super(Obstacle, self).__init__(gameplay, x, y, size, image)
        self.rect = gameplay.scale_image(self.image, 60).get_rect()
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.distance = distance
        self.owner = None

    def set_owner(self, owner):
        self.owner = owner

    def move(self, direction, timedelta, step = 0):
        super().move(direction, timedelta, step)
        self.distance -= 2


class Weapon(Instance):

    def __init__(self, gameplay, type, image):
        self.type = type
        self.fire_rate_waiting = False
        self.fire_rate_waiting_time = 0.0
        self.reload_waiting = False
        self.reload_waiting_time = 0.0

        super(Weapon, self).__init__(gameplay, -1, -1, 0, image)

        if type == "gun":
            self.fire_rate = 3.0
            self.reload_time = 10.0
            self.max_ammo = 30
            self.distance = 100.0
            self.damage = 20.0
            self.speed = 15.0
            self.bullet_size = 40
        elif type == "shotgun":
            self.fire_rate = 8.0
            self.reload_time = 10.0
            self.max_ammo = 8
            self.distance = 100.0
            self.damage = 20.0
            self.speed = 20.0
            self.bullet_size = 50
        elif type == "thomson":
            self.fire_rate = 1.0
            self.reload_time = 20.0
            self.max_ammo = 30
            self.distance = 100.0
            self.damage = 5.0
            self.speed = 20.0
            self.bullet_size = 35
        else:  # hand
            self.fire_rate = 1.0
            self.reload_time = 2.0
            self.max_ammo = 1
            self.distance = 40.0
            self.damage = 2.0
            self.speed = 0.0
            self.bullet_size = 0


        self.ammo = self.max_ammo * 2
        self.magazine = self.max_ammo

    def shot(self, x=0, y=0, angle=0, image=None):
        bullet = None
        if self.type != 'hand':
            bullet = Bullet(self.gameplay, x, y, self.bullet_size, image, angle, self.speed, self.damage, self.distance)
            self.magazine -= 1
        self.fire_rate_waiting = True
        return bullet, self.ammo + self.magazine

    def reload(self):
        if self.reload_waiting:
            self.reload_waiting = False
            self.reload_waiting_time = self.reload_time
        elif self.magazine < self.max_ammo:
            self.reload_waiting = True
            self.reload_waiting_time = 0.0

    def wait(self):
        if self.fire_rate_waiting:
            self.rate_wait()

        if self.reload_waiting:
            self.reload_wait()

    def rate_wait(self):
        if self.fire_rate_waiting_time < self.fire_rate:
            self.fire_rate_waiting_time += 1
        else:
            self.fire_rate_waiting_time = 0.0
            self.fire_rate_waiting = False

    def reload_wait(self):
        if self.reload_waiting_time < self.reload_time and self.ammo > 0:
            self.reload_waiting_time += 1
        elif self.ammo > 0:
            difference = self.max_ammo - self.magazine
            difference = difference if difference < self.ammo else self.ammo
            self.magazine += difference
            self.ammo -= difference

            self.reload_waiting = False
            self.reload_waiting_time = 0.0

    def is_able_to_shot(self):
        return not self.fire_rate_waiting and self.magazine > 0 and not self.reload_waiting

