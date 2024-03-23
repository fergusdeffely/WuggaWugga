from enum import Enum
import pygame
import pygame_gui
from globals import *
from timeline_logger import timeline_logger
from level import LevelRunState


class WuggaUIButton(pygame_gui.elements.UIButton):

    def __init__(self, rect, text, manager, anchors, name):
        super().__init__(relative_rect=rect, text=text, manager=manager, anchors=anchors)
        self._name = name


    def on_clicked(self, ui, session):
        log(4, f"WuggaUIButton: on_clicked: {self._name}")
        if self._name == "pause_button":
            ticks = pygame.time.get_ticks()
            if ui.level.runstate == LevelRunState.RUNNING:
                ui.level.paused_at = ticks
                timeline_logger.log(f"Timeline.pause: at:{ticks}", ticks)
                session.timeline.pause()
                ui.pause()              

                self.set_text("Unpause")
            else:               
                gap = ticks - ui.level.paused_at
                timeline_logger.log(f"Timeline.unpause: at:{ticks}, gap:{gap}", ticks)
                session.unpause(gap)
                ui.level.unpause(gap, ticks)

                self.set_text("Pause")
