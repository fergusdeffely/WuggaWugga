import pygame, sys
import pygame_gui
from globals import *

from wugga_io import Output
from ui import UI
from timeline_logger import timeline_logger
from timeline import Timeline
from timeline_event import TimelineEvent
from tile import Tile
from level import Level
from level import LevelRunState
from audio import Audio
from mouse import Mouse


class Game():

    def __init__(self):

        # Pygame setup
        pygame.init()
        
        screen = pygame.display.set_mode(SCREEN_SIZE, flags=pygame.NOFRAME)
        self._out = Output(screen, Audio())        

        self._timeline = Timeline()

        ui_manager = pygame_gui.UIManager(SCREEN_SIZE, "config/ui_theme.json")

        mouse = Mouse()
        
        # this will eventually be moved to a level select screen
        level = Level("config/level1.json", self._out, self._timeline)

        self._ui = UI(ui_manager, self._out, mouse, level)


    def run(self):
        clock = pygame.time.Clock()
        cycle = 0

        while True:
            time_delta = clock.tick(FRAMES_PER_SECOND)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    log(5, f"Event: MouseButtonUp : {event.button} at {screen_to_grid(event.pos, self._ui.level.grid_offset)}")
                    if event.button == 1:
                        if self._ui.level.runstate == LevelRunState.RUNNING:
                            self._ui.level.handle_click_button1(cycle, event.pos, self._timeline, self._ui.mouse)
                    if event.button == 3:
                        if self._ui.level.runstate == LevelRunState.RUNNING:
                            self._ui.level.handle_click_button2(cycle, event.pos, self._ui.mouse)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._ui.handle_keydown(event.key, self._ui.mouse)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    log(5, f"Event{event.type}: pygame_gui.UI_BUTTON_PRESSED : {event}")
                    self._ui.handle_gui_event(cycle, event, self._timeline)

                self._ui.manager.process_events(event)

            self._timeline.update(cycle)
            self._out.video.fill("black")

            self._ui.update(cycle, time_delta)
            self._ui.draw(self._out.video)

            pygame.display.update()

            cycle += 1

Game().run()