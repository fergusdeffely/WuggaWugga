import pygame, sys
import pygame_gui
import globals as g

from ui.game_screen import GameScreen
from ui.menu_screen import MenuScreen
from audio import Audio


class Game():

    def __init__(self):

        # Pygame setup
        pygame.init()
        
        self._video = pygame.display.set_mode(g.SCREEN_SIZE, flags=pygame.NOFRAME)
        self._audio = Audio()

        self._screen = MenuScreen()
        self._transition = None


    def run(self):
        clock = pygame.time.Clock()

        while True:
            time_delta = clock.tick(g.FRAMES_PER_SECOND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                command = self._screen.process_event(event)
                if command is not None:
                    g.log(3, f"game.run: received menucommand: {command}...")
                    self._transition = command.transition
                    self._screen = command.screen

            self._video.fill("black")

            if self._transition:
                # screen transition is in progress
                self._transition.update()
                self._transition.draw(self._video)
                if self._transition.complete:
                    self._transition = None
            else:
                self._screen.update(time_delta, self._audio)
                self._screen.draw(self._video)

            pygame.display.update()
            

Game().run()