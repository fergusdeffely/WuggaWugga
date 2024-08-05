import pygame
import pygame_gui
from pygame_gui import UIManager
from enum import Enum
import globals as g
from ui.main_menu import MainMenu
from ui.main_menu import MainMenuOptions


class MenuScreen():

    def __init__(self):
        self._ui_manager = UIManager(g.SCREEN_SIZE, "config/ui_theme.json")
        self.menu = MainMenu(self._ui_manager)


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            g.log(5, f"menu_screen.process_event: MouseButtonUp : {event.button} at {event.pos}")
            if event.button == 1:
                self.menu.handle_click_button1(event.pos)
            if event.button == 3:
                self.menu.handle_click_button2(event.pos)

        if event.type == pygame.KEYDOWN:
            self.menu.handle_keydown(event.key)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            result = self.menu.handle_button_pressed(event)
            g.log(3, f"menu_screen.process_event: result: {result}")
            if isinstance(result, MainMenuOptions):
                g.log(3, f"menu_screen.process_event: yes - it is a MainMenuOptions!")
                return result
            else:
                g.log(3, f"menu_screen.process_event: no - not a MainMenuOptions!")

        self._ui_manager.process_events(event)

        return None


    def update(self, time_delta, audio):
        self._ui_manager.update(time_delta / 1000.0)


    def draw(self, surface):
        self._ui_manager.draw_ui(surface)
        