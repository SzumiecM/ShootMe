import pygame
from Gameplay import Gameplay
import time
from network import Network


class Window:
    # starting settings
    name = 'surviv'

    def __init__(self):
        pygame.init()
        # setting window's name
        pygame.display.set_caption(self.name)

        self.gameplay = Gameplay()
        self.height = self.gameplay.get_screen_height()
        self.width = self.gameplay.get_screen_width()

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
            p1 = [self.gameplay.allPlayersToPickle[player], self.gameplay.bulletsToPickle, self.gameplay.boxes]
            self.gameplay.boxes = []
            self.gameplay.bulletsToPickle = []
            p2 = n.send(p1)
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

            # refreshes screen
            pygame.display.flip()
