import pygame
import os
import json
import random
from Instances import *
from Player import Player
import math


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

    max_players = None
    players = []
    # Player on which camera is focused
    current_focus = None

    max_obstacle_size = None
    min_obstacle_size = None
    obstacles = []
    images = {}
    pick_ups = []
    visible = []

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
        self.current_focus = self.players[0]

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
                scaled = self.scale_image(image, size)
                obstacle = Rock(self, x, y, size, scaled)
            else:
                image = self.images['rock']
                scaled = self.scale_image(image, size)
                obstacle = Rock(self, x, y, size, scaled)

            if not self.check_if_collide(obstacle):
                self.obstacles.append(obstacle)
                obstacles_area += obstacle.get_area()

    def check_if_collide(self, obstacle):
        for curr_obstacle in self.obstacles:
            if self.collide(obstacle, curr_obstacle):
                return True

        return False

    def generate_players(self):
        for i in range(0, self.max_players):
            player = self.create_player()
            while self.check_if_collide(player):
                player = self.create_player()
            self.players.append(player)

    def create_player(self):
        x = random.uniform(0, self.map_size)
        y = random.uniform(0, self.map_size)
        size = self.min_obstacle_size + (self.min_obstacle_size + self.max_obstacle_size) // 3
        image = self.images["player&hand"]
        scaled = self.scale_image(image, size)
        player = Player(self, x, y, size, scaled)
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
        if left:
            self.attack(self.current_focus)


    def play(self, timedelta):
        for key in self.controling_keys:
            # if any from WSAD pressed
            if self.controling_keys[key]:
                for i in range(2):
                    self.move_player(self.current_focus, key, timedelta)
                    timedelta /= 2
        self.rotate_player(self.current_focus)

        self.visible = []

    def move_player(self, player, key, timedelta):
        # move there by passing key string
        player.move(key, timedelta)
        for obstacles in self.obstacles:
            # if player collide after movement
            # move they back (by passing negative time)
            if self.collide(self.current_focus, obstacles):
                player.move(key, -timedelta)

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
            angle = math.pi * player.angle/180
            distance = player.weapon.distance
            x = player.x + 0.75*player.size - math.sin(angle) * (2*distance)
            y = player.y + 0.75*player.size - math.cos(angle) * (2*distance)
            print(x, y)
            attack_zone = pygame.Rect(x, y, distance, distance)


            for obstacle in self.obstacles:
                if self.collide(obstacle, attack_zone):
                    obstacle.get_damge(player.weapon.damage)
                    print(obstacle.size)
        else:
            pass

    def drop(self, obstacle):
        self.obstacles.remove(obstacle)
        pass

    # Function checks if an object is in range of a screen.
    # Object should be displayed only if it is in range.
    def check_if_on_screen(self, instance):
        view_rect = self.get_view_rectangle()
        visivility_range = instance.get_visibility_range()
        h = visivility_range.h
        w = visivility_range.w
        zoom = self.current_focus.zoom
        zoomed_width = int(w / zoom)
        zoomed_height = int(h / zoom)

        moved = visivility_range.move(-zoomed_width, -zoomed_height)
        if view_rect.colliderect(moved):
            self.visible.append(instance)
            return True
        return False

    # draws map
    # then draws players (if they are within the range of the screen)
    # then obstacles.
    def draw(self):
        self.draw_map()

        for player in self.players:
            if self.check_if_on_screen(player):
                self.draw_instance(player)

        for obstacle in self.obstacles:
            if self.check_if_on_screen(obstacle):
                self.draw_instance(obstacle)

        for pick_up in self.pick_ups:
            if self.check_if_on_screen(pick_up):
                self.draw_instance(pick_up)

        player = self.current_focus

        #pygame.draw.rect(self.screen, (200, 100, 50), attack_zone)

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
    def draw_instance(self, instance):

        zoom = self.current_focus.zoom
        image = instance.get_image()
        (width, height) = image.get_rect().size
        zoomed_width = int(width / zoom)
        zoomed_height = int(height / zoom)

        zoomed_image = pygame.transform.scale(image, (zoomed_width, zoomed_height))
        (x, y) = self.calculate_position(instance)
        player_rect = self.current_focus.image.get_rect()
        p_w = player_rect.w
        p_h = player_rect.h
        pos = (x / zoom - p_w / 2, y / zoom - p_h / 2)
        rotated_image = pygame.transform.rotate(zoomed_image, instance.angle)
        self.screen.blit(rotated_image, pos)

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
