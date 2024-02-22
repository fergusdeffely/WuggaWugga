import pygame, sys
import pygame_gui
from globals import *

from session import Session
from session import GameState
from wugga_io import Output
from ui import UI
from timeline import Timeline
from timeline_event import TimelineEvent
from tile import Tile
from level_data import level_map
from level import Level
from audio import Audio
from mouse import Mouse


class Game():

    def __init__(self):

        # Pygame setup
        pygame.init()
        self.clock = pygame.time.Clock()

        screen = pygame.display.set_mode(SCREEN_SIZE)
        self.out = Output(screen, Audio())
        self.level = Level(level_map, self.out)

        timeline = Timeline()
        spawn_beatbug_event = TimelineEvent(pygame.time.get_ticks(), 
                                            self.level.spawn_beatbug, 
                                            0, 2000)
        timeline.add_event(spawn_beatbug_event)

        self.session = Session(timeline, GameState.RUNNING)
        ui_manager = pygame_gui.UIManager(SCREEN_SIZE, "ui_theme.json")
        
        self.ui = UI(ui_manager, self.out.video)
        self.mouse = pygame.sprite.GroupSingle(Mouse())
        

    def run(self):
        while True:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    print(f"Event: MouseButtonUp : {event.button} at {screen_to_grid(event.pos)}")
                    if event.button == 1:
                        if self.session.gamestate == GameState.RUNNING:
                            self.level.handle_click(event.pos, self.session.selected_assistant)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    print ("Event: pygame_gui.UI_BUTTON_PRESSED :")
                    self.ui.handle_gui_event(event, self.session)

                self.ui.manager.process_events(event)

            self.session.timeline.update()
            self.out.video.fill("black")

            self.level.update(self.session.gamestate, self.out.audio)
            self.level.draw(self.out.video)

            self.ui.update(time_delta)
            self.ui.draw(self.out.video)

            self.mouse.update()
            self.mouse.draw(self.out.video)

            pygame.display.update()

Game().run()