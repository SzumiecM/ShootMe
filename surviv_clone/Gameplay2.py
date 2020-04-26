import pygame
import os
import json
import random
from Instances import *
import math
import itertools


class Gameplay:
    isOpen = True
    screen = None
    settings_path = 'data/settings.json'

    screen_height = None
    screen_width = None
    height = None
    width = None
    map_size = None
    density = None

    visibility_range = None

    max_players = 2
    players = []
    # Player on which camera is focused
    current_focus = None

    max_obstacle_size = None
    min_obstacle_size = None

    obstacles = []
    images = {}
    pick_ups = []
    visible = []
    bullets = []

    allPlayersToPickle = []
    bulletsToPickle = []

    c_f = 1

    controling_keys = {
        'up': False,
        'down': False,
        'right': False,
        'left': False
    }

    def __init__(self):
        self.load_settings()
        self.load_data()
        self.generate_obstacles()
        self.generate_players()
        self.current_focus = self.players[self.c_f]
        self.pickle_players()

        #self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

        zoom = self.current_focus.zoom
        coeff = 1
        self.width = coeff * zoom * self.screen_width
        self.height = coeff * zoom * self.screen_height
        x = self.current_focus.get_x()
        y = self.current_focus.get_y()
        self.visibility_range = pygame.Rect(0, 0, self.width, self.height).move(x - self.width / 2, y - self.height / 2)

    def set_screen(self, screen):
        self.screen = screen

    def get_screen_height(self):
        return self.screen_height

    def get_screen_width(self):
        return self.screen_width

    def load_settings(self):
        # loading settings from json file
        # json - comfortable data formatting
        with open(self.settings_path) as f:
            data = json.load(f)
        self.screen_height = data['height']
        self.screen_width = data['width']
        self.max_players = data['max_players']
        self.map_size = data['map_size']
        self.density = data['density']
        self.max_obstacle_size = data['max_obstacle_size']
        self.min_obstacle_size = data['min_obstacle_size']

    def load_data(self):
        # loading images
        for file in os.listdir(os.path.abspath(os.getcwd()) + os.sep + "images"):
            if file.endswith('png'):
                name = os.path.basename(file)  # gives filename without a path
                name = os.path.splitext(name)[0]  # gives ('name', 'ext'), then we choose first element
                self.images[name] = pygame.image.load(os.getcwd() + os.sep + 'images' + os.sep + file)
                if '&' in name:
                    Player.add_image(name, self.images[name])

        # resizing the map according to settings
        map_surf = self.images['background']
        self.images['background'] = pygame.transform.scale(map_surf, (self.map_size, self.map_size))

    # checks if two objects collide
    def collide(self, obstacle_1, obstacle_2):
        if isinstance(obstacle_2, pygame.Rect):
            return obstacle_1.get_collider().colliderect(obstacle_2)
        else:
            return pygame.sprite.collide_rect(obstacle_1, obstacle_2)

    def scale_image(self, image, size):
        width = image.get_rect().width
        height = image.get_rect().height
        scaled_width = int(width * size / self.max_obstacle_size)
        scaled_height = int(height * size / self.max_obstacle_size)
        image = pygame.transform.scale(image, (scaled_width, scaled_height))
        return image

    def generate_obstacles(self):
        # generate obstacles till we get the wanted obstacles' density

        obstacles_area = 0
        map_range = self.map_size * self.map_size
        while obstacles_area < self.density * map_range:
            type = random.randint(0, 2)
            x = random.uniform(0, self.map_size)
            y = random.uniform(0, self.map_size)
            size = random.randint(self.min_obstacle_size, self.max_obstacle_size)
            if type == 0:
                image = self.images['rock']
                obstacle = Rock(self, x, y, size, image)
            else:
                image = self.images['rock']
                obstacle = Rock(self, x, y, size, image)

            if not self.check_if_collide(obstacle):
                self.obstacles.append(obstacle)
                obstacles_area += obstacle.get_area()

    def check_if_collide(self, obstacle):
        for curr_obstacle in self.obstacles:
            if self.collide(obstacle, curr_obstacle):
                return True

        return False

    def get_players(self):
        return self.players

    def generate_players(self):
        for i in range(0, self.max_players):
            player = self.create_player()
            while self.check_if_collide(player):
                player = self.create_player()
            self.players.append(player)
        return self.players

    def create_player(self):
        x = random.uniform(0, self.map_size)
        y = random.uniform(0, self.map_size)
        size = self.min_obstacle_size + (self.min_obstacle_size + self.max_obstacle_size) // 3
        image = self.images["player&hand"]
        player = Player(self, x, y, size, image)
        player.set_weapon(Weapon(self, 'hand', None))
        return player

    def has_quited(self):
        return not self.isOpen

    def on_press(self, event):
        pressed_keys = pygame.key.get_pressed()
        (left, middle, right) = pygame.mouse.get_pressed()

        # the construction below is equivalent
        # to that one:
        #   if pressed_keys[pygame.K_w]:
        #        self.controling_keys['up'] = True
        #   else:
        #       self.controling_keys['up'] = False
        # but shorter
        #

        self.controling_keys['up'] = True if pressed_keys[pygame.K_w] else False
        self.controling_keys['down'] = True if pressed_keys[pygame.K_s] else False
        self.controling_keys['right'] = True if pressed_keys[pygame.K_d] else False
        self.controling_keys['left'] = True if pressed_keys[pygame.K_a] else False
        self.controling_keys['left_mouse'] = True if left else False

        if pressed_keys[pygame.K_r] and self.current_focus.weapon.type != 'hand':
            self.current_focus.weapon.reload()

        if pressed_keys[pygame.K_e]:
            self.generate_pick_ups(self.current_focus.x, self.current_focus.y, self.current_focus.weapon.type)
            self.pick_up(self.current_focus)

        if pressed_keys[pygame.K_q]:
            self.generate_pick_ups(self.current_focus.x, self.current_focus.y, self.current_focus.weapon.type)
            self.current_focus.set_weapon(Weapon(self, 'hand', None))

        if pressed_keys[pygame.K_y]:
            index = self.players.index(self.current_focus) + 1
            index = index if index < len(self.players) else 0
            self.current_focus = self.players[index]

    def play(self, timedelta):
        for key in ['right', 'left', 'up', 'down']:
            # if any from WSAD pressed
            if self.controling_keys[key]:
                for i in range(2):
                    self.current_focus.move(key, timedelta)
                    self.perform_collision(self.current_focus, lambda k, t: self.current_focus.move(k, -t),
                                           (key, timedelta))
                    timedelta /= 2
                timedelta *= 4

        if self.controling_keys['left_mouse']:
            self.attack(self.current_focus)

        for player in self.players:
            player.weapon.wait()

        self.rotate_player(self.current_focus)

        for bullet in self.bullets:
            self.move_bullet(bullet, timedelta)
            self.perform_collision(bullet, self.collide_bullet, (bullet,), obstacle_as_arg=True, works_for_players=True)

        for obstacle in itertools.chain(self.players, self.bullets):
            if not (0 < obstacle.x < self.map_size and 0 < obstacle.y < self.map_size):
                if isinstance(obstacle, Player):
                    self.players.remove(obstacle)
                    self.current_focus = None
                else:
                    if obstacle in self.bullets:
                        self.bullets.remove(obstacle)
        self.visible = []
        self.pickle_players()

    def collide_bullet(self, obstacle, bullet):
        obstacle.get_damage(bullet.damage)
        if bullet in self.bullets:
            self.bullets.remove(bullet)
            self.bulletsToPickle.remove(x for x in self.bulletsToPickle if x['x'] == bullet.x and x['y'] == bullet.y)

    def move_bullet(self, bullet, timedelta):
        angle = bullet.angle
        step = bullet.speed * timedelta / 100
        x_step = -step * math.sin(angle)
        y_step = -step * math.cos(angle)
        bullet.move('right', x_step)
        bullet.move('down', y_step)
        if bullet.distance < 0:
            self.bullets.remove(bullet)
            self.bulletsToPickle.remove(x for x in self.bulletsToPickle if x['x'] == bullet.x and x['y'] == bullet.y)

    def pickle_bullet(self, bullet):
        self.bulletsToPickle.append({
            'angle': bullet.angle,
            'speed': bullet.speed,
            'damage': bullet.damage,
            'distance': bullet.distance
        })

    def pickle_players(self):
        # self.allPlayersToPickle = []
        # for player in self.players:
        #     self.allPlayersToPickle.append({
        #         'x': player.x,
        #         'y': player.y,
        #         'weapon': player.weapon.type,
        #         'life': player.life
        #     })

        self.allPlayersToPickle = {
                    'x': self.current_focus.x,
                    'y': self.current_focus.y,
                    'weapon': self.current_focus.weapon.type,
                    'life': self.current_focus.life
        }

    def unPickle_players(self, data):
        for i in range(len(self.players)):
            if self.c_f != i:
                self.players[i].x = data[0][i]['x']
                self.players[i].y = data[0][i]['y']
                self.players[i].weapon.type = data[0][i]['weapon']
                self.players[i].life = data[0][i]['life']

    # if obstacle arg is True it uses obstacle as a first argument
    def perform_collision(self, instance, function, args, obstacle_as_arg=False, works_for_players=False):
        for obstacle in itertools.chain(self.obstacles, self.players):
            # if obstacle collides after movement
            # performs a function wtih args given as argument)
            if not isinstance(obstacle, Player) or (works_for_players and isinstance(obstacle, Player)):
                if self.collide(instance, obstacle):
                    if obstacle_as_arg:
                        function(obstacle, *args)
                    else:
                        function(*args)

    def rotate_player(self, player):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        player_x = self.screen_width / 2
        player_y = self.screen_height / 2
        d_x = mouse_x - player_x
        d_y = - (mouse_y - player_y)
        angle = 180 * math.atan2(d_y, d_x) / math.pi - 90
        player.angle = angle

    def attack(self, player):
        if player.weapon.type == 'hand':
            # creating a box by the front of a player
            # to give a damage
            angle = math.pi * player.angle / 180
            distance = player.weapon.distance
            x = player.x + 0.75 * player.size - math.sin(angle) * (2 * distance)
            y = player.y + 0.75 * player.size - math.cos(angle) * (2 * distance)
            attack_zone = pygame.Rect(x, y, distance, distance)
            # hand shoots to simulate waiting for a next punch
            player.shot()
            for obstacle in itertools.chain(self.obstacles, self.players):
                if self.collide(obstacle, attack_zone) and obstacle != player:
                    obstacle.get_damage(player.weapon.damage)
        else:
            if player.weapon.is_able_to_shot():
                bullet = player.shot(self.images['rock'])
                self.bullets.append(bullet)
                self.pickle_bullet(bullet)

    def get_bullets(self):
        return self.bullets

    def drop(self, obstacle):
        x = obstacle.x
        y = obstacle.y
        for objects in [self.obstacles, self.players]:
            if obstacle in objects:
                objects.remove(obstacle)
                break

        type = obstacle.weapon.type if isinstance(obstacle, Player) else None

        self.generate_pick_ups(x, y, type)

    def generate_pick_ups(self, x, y, type=None):
        if type == 'hand':
            return
        size = (self.min_obstacle_size + self.max_obstacle_size) / 2
        x = x + random.uniform(-self.min_obstacle_size, self.min_obstacle_size)
        y = y + random.uniform(-self.min_obstacle_size, self.min_obstacle_size)

        if type is None:
            type = random.randint(0, 3)
            if type == 0:
                name = 'gun'
            elif type == 1:
                name = 'shotgun'
            else:
                name = 'thomson'
        else:
            name = type

        image = self.images[name]

        pick_up = Pick_up(self, x, y, size, image, name)
        self.pick_ups.append(pick_up)

    def pick_up(self, player):
        for pick_up in self.pick_ups:
            if self.collide(player, pick_up):
                name = pick_up.name
                weapon = Weapon(self, name, pick_up.original_image)
                player.set_weapon(weapon)
                self.pick_ups.remove(pick_up)
                break

    def update(self, data):
        self.unPickle_players(data)

    # Function checks if an object is in range of a screen.
    # Object should be displayed only if it is in range.
    def check_if_on_screen(self, instance):
        view_rect = self.get_view_rectangle()
        visibility_range = instance.get_visibility_range()
        h = visibility_range.h
        w = visibility_range.w
        zoom = self.current_focus.zoom
        zoomed_width = int(w / zoom)
        zoomed_height = int(h / zoom)

        moved = visibility_range.move(-zoomed_width, -zoomed_height)
        if view_rect.colliderect(moved):
            self.visible.append(instance)
            return True
        return False

    # draws map
    # then draws players (if they are within the range of the screen)
    # then obstacles.
    def draw(self):
        self.draw_map()

        for instance in itertools.chain(self.players, self.obstacles, self.pick_ups, self.bullets):
            if self.check_if_on_screen(instance):
                self.draw_instance(instance)

        self.draw_hud()
        player = self.current_focus

        # pygame.draw.rect(self.screen, (200, 100, 50), attack_zone)

    def draw_hud(self):
        text = ''
        text += 'Life: {}\n'.format(self.current_focus.life)
        text += 'Weapon: {}\n'.format(self.current_focus.weapon.type)
        if self.current_focus.weapon.type != 'hand':
            text += 'Magazine: {}\n'.format(self.current_focus.weapon.magazine)
            text += 'Ammo: {}\n'.format(self.current_focus.weapon.ammo)
        if self.current_focus.weapon.magazine == 0:
            text += 'NO AMMUNITION\n'
        if self.current_focus.weapon.reload_waiting:
            text += 'RELOADING\n'

        lines = text.splitlines()

        font_size = 32
        for i, l in enumerate(lines):
            line = self.font.render(l, 0, (0, 0, 0))
            self.screen.blit(line, (20, 20 + font_size * i))

    # calculates relative position to display on screen
    # x and y of instances are absolute positions on the map
    def calculate_position(self, instance):
        x = instance.x
        y = instance.y
        focus_x = self.current_focus.get_x()
        focus_y = self.current_focus.get_y()
        screen_x = x - focus_x + self.width / 2
        screen_y = y - focus_y + self.height / 2
        return screen_x, screen_y

    #
    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def draw_instance(self, instance):

        zoom = self.current_focus.zoom
        image = instance.get_image()
        (width, height) = image.get_rect().size
        zoomed_width = int(width / zoom)
        zoomed_height = int(height / zoom)

        image = pygame.transform.scale(image, (zoomed_width, zoomed_height))
        (x, y) = self.calculate_position(instance)
        player_rect = self.current_focus.image.get_rect()
        p_w = player_rect.w
        p_h = player_rect.h
        pos = (x / zoom - p_w / 2, y / zoom - p_h / 2)
        image = pygame.transform.rotate(image, instance.angle)

        self.screen.blit(image, pos)

    def get_view_rectangle(self):
        x = self.current_focus.get_x()
        y = self.current_focus.get_y()
        beg_x = (x - self.width / 2)
        beg_y = (y - self.height / 2)
        return pygame.Rect(beg_x, beg_y, self.width, self.height)

    def draw_map(self):

        # getting the position of a player
        view_rect = self.get_view_rectangle()
        view = pygame.Surface((view_rect.w, view_rect.h))
        view.blit(self.images['background'], (-view_rect.x, -view_rect.y))
        view = pygame.transform.scale(view, (self.screen_width, self.screen_height))

        self.screen.blit(view, (0, 0))
