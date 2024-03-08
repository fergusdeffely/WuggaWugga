import pygame, sys
import pygame_gui
from globals import *

from session import Session
from session import GameState
from wugga_io import Output
from ui import UI
from timeline_logger import timeline_logger
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
        level = Level(level_map, self.out)

        timeline = Timeline()
        self.t0 = pygame.time.get_ticks()
        timeline_logger.start(self.t0)
        spawn_beatbug_event = TimelineEvent(self.t0, level.spawn_beatbug, 0, 2000)
        timeline.add_event(spawn_beatbug_event)

        self.session = Session(timeline, timeline_logger, self.t0, GameState.RUNNING)
        ui_manager = pygame_gui.UIManager(SCREEN_SIZE, "ui_theme.json")
        
        mouse = pygame.sprite.GroupSingle(Mouse())
        self.ui = UI(ui_manager, self.out, mouse, level)
        

    def run(self):
        while True:
            frame_ticks = pygame.time.get_ticks()
            time_delta = self.clock.tick(50)
            if LOG_FRAME_DELTAS:
                timeline_logger.log(f"loop:delta={time_delta}", frame_ticks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    log(3, f"Event: MouseButtonUp : {event.button} at {screen_to_grid(event.pos)}")
                    if event.button == 1:
                        if self.session.gamestate == GameState.RUNNING:
                            self.ui.level.handle_click_button1(frame_ticks, event.pos, self.session, self.ui.mouse.sprite)
                    if event.button == 3:
                        if self.session.gamestate == GameState.RUNNING:
                            self.ui.level.handle_click_button2(frame_ticks, event.pos, self.session, self.ui.mouse.sprite)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ui.handle_keydown(event.key, self.session)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    log(3, f"Event{event.type}: pygame_gui.UI_BUTTON_PRESSED : {event}")
                    self.ui.handle_gui_event(event, self.session)

                if event.type == CHANNEL_READY_EVENT:
                    log(3, f"Event{event.type}: Channel Ready: {event}")
                    self.ui.level.on_channel_ready(event.code)

                self.ui.manager.process_events(event)

            self.session.timeline.update(frame_ticks)
            self.out.video.fill("black")

            self.ui.update(frame_ticks, time_delta, self.session)
            self.ui.draw(self.out.video, self.session)

            pygame.display.update()

Game().run()