import pygame
from pygame_gui.elements import UIButton
from enum import Enum
import globals as g

class MainMenuOptions(Enum):
    START      = 0
    CONTINUE   = 1
    QUIT       = 2

class MainMenu():

    def __init__(self, ui_manager):
        self._ui_manager = ui_manager
        self._create_menu_options(["Continue", "New Game", "Options", "Help"])
        self._buttons = {}


    def _create_menu_options(self, options):
        x = (g.SCREEN_WIDTH_PIXELS - g.MENU_BUTTON_WIDTH) / 2
        block_height = g.MENU_BUTTON_HEIGHT * len(options) + g.MENU_BUTTON_SEPARATOR * (len(options) - 1)
        y = (g.SCREEN_HEIGHT_PIXELS - block_height) / 2
        for option in options:
            UIButton(relative_rect=pygame.Rect(x, y, g.MENU_BUTTON_WIDTH, g.MENU_BUTTON_HEIGHT),
                     text=option,
                     manager=self._ui_manager)
            y = y + g.MENU_BUTTON_HEIGHT + g.MENU_BUTTON_SEPARATOR


    def handle_button_pressed(self, event):
        g.log(3, f"MainMenu.on_button_pressed: text: {event.ui_element.text}")
        return MainMenuOptions.START


    def handle_click_button1(self, event_pos):
        g.log(4, f"MainMenu.handle_click_button1: at position: {event_pos}")


    def handle_click_button2(self, event_pos):
        g.log(4, f"MainMenu.handle_click_button2: at position: {event_pos}")
        

    def handle_keydown(self, key):
        g.log(4, f"MainMenu.handle_keydown: key: {key}")


