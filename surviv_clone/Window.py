import pygame
from Gameplay import Gameplay
import time

class Window:
    # starting settings
    name = 'surviv'
    music_path = None

    def __init__(self):
        self.gameplay = Gameplay()
        self.height = self.gameplay.get_screen_height()
        self.width = self.gameplay.get_screen_width()

        pygame.init()
        #setting window's name
        pygame.display.set_caption(self.name)

        # !!!
        if self.music_path is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.gameplay.set_screen(self.screen)

    def start(self):
        stopped = False
        clock = pygame.time.Clock()
        while not stopped:
            # Triggering events: using mouse and keyboard
            for event in pygame.event.get():
                self.gameplay.on_press(event)

                # Exiting a game either by closing event or by game option
                if event.type == pygame.QUIT or self.gameplay.has_quited():
                    #self.gameplay.quit()
                    stopped = True

            timedelta = 0.4*clock.tick(60)
            self.gameplay.play(timedelta)
            self.gameplay.draw()

            # refreshes screen
            pygame.display.flip()
            #input("xD")

