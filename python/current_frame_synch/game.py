import pygame, sys
import pygame_gui
import globals as g

from wugga_io import Output
from ui.game_screen import GameScreen
from ui.menu_screen import MenuScreen
from audio import Audio


class Game():

    def __init__(self):

        # Pygame setup
        pygame.init()
        
        surface = pygame.display.set_mode(g.SCREEN_SIZE, flags=pygame.NOFRAME)
        self._out = Output(surface, Audio())

        self._screen = MenuScreen()


    def run(self):
        clock = pygame.time.Clock()

        while True:
            time_delta = clock.tick(g.FRAMES_PER_SECOND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                screen = self._screen.process_event(event)
                if screen is not None:
                    g.log(3, f"game.run: switching screen: {screen}...")
                    self._screen = screen

            self._out.video.fill("black")

            self._screen.update(time_delta, self._out.audio)
            self._screen.draw(self._out.video)

            pygame.display.update()
            

Game().run()