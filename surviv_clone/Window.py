import pygame
from Gameplay import Gameplay
import time
from network import Network


class Window:
    # starting settings
    name = 'surviv'
    music_path = None

    def __init__(self):
        pygame.init()
        # setting window's name
        pygame.display.set_caption(self.name)

        self.gameplay = Gameplay()
        self.height = self.gameplay.get_screen_height()
        self.width = self.gameplay.get_screen_width()

        # to play a music in a background
        if self.music_path is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.gameplay.set_screen(self.screen)

    def start(self):
        stopped = False
        n = Network()
        base = n.getP()
        data = base[0]
        player = base[1]
        boxes = base[2]
        self.gameplay.c_f = player  # ustawiamy id gracza
        self.gameplay.current_focus = self.gameplay.players[player]
        self.gameplay.sync_windows(data)
        self.gameplay.generate_obst_from_data(boxes)
        clock = pygame.time.Clock()
        pygame.font.init()
        while not stopped:
            #print(player)
            p1 = [self.gameplay.allPlayersToPickle[player], self.gameplay.bulletsToPickle, self.gameplay.boxes]
            self.gameplay.boxes = []
            self.gameplay.bulletsToPickle = []
            #print(p1)
            p2 = n.send(p1)
            #print(p2)
            self.gameplay.update(p2)

            # Triggering events: using mouse and keyboard
            for event in pygame.event.get():
                self.gameplay.on_press(event)

                # Exiting a game either by closing event or by game option
                if event.type == pygame.QUIT or self.gameplay.has_quited():
                    # self.gameplay.quit()
                    stopped = True

            timedelta = 0.4 * clock.tick(60)
            self.gameplay.play(timedelta)
            self.gameplay.pickle_player(self.gameplay.c_f)
            self.gameplay.draw()

            # print('KURWA')
            # for p in self.gameplay.players:
            #     print(str(p.x) + ' | ' + str(p.y))

            # refreshes screen
            pygame.display.flip()
