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


    def on_clicked(self, cycle, ui, timeline):
        log(4, f"WuggaUIButton: on_clicked: {self._name}")
        if self._name == "pause_button":
            if ui.level.runstate == LevelRunState.RUNNING:
                ui.level.paused_at = cycle
                timeline_logger.log(f"Timeline.pause", cycle)
                timeline.pause()
                ui.pause()

                self.set_text("Unpause")
            else:               
                paused_cycles = cycle - ui.level.paused_at
                timeline_logger.log(f"Timeline.unpause: paused for: {paused_cycles}", cycle)
                timeline.unpause(paused_cycles)
                ui.level.unpause(paused_cycles)

                self.set_text("Pause")
