import pygame
import pygame_gui
from pygame_gui import UIManager
from enum import Enum
import globals as g
from ui.main_menu import MainMenu

class MenuScreen():

    def __init__(self):
        self._ui_manager = UIManager(g.SCREEN_SIZE, "config/ui_theme.json")
        self.menu = MainMenu(self._ui_manager)


    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.menu.handle_keydown(event.key)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            return self.menu.handle_button_pressed(event)

        self._ui_manager.process_events(event)

        return None


    def update(self, time_delta, audio):
        self._ui_manager.update(time_delta / 1000.0)


    def draw(self, surface):
        self._ui_manager.draw_ui(surface)
        