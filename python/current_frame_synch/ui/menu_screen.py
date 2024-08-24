import pygame
import pygame_gui
from pygame_gui import UIManager
from enum import Enum

import globals as g
from enums import MenuOption, TransitionType
from ui.main_menu import MainMenu
from ui.screen_transition import ScreenTransition
from ui.rising_flood_transition import RisingFloodTransition
from ui.game_screen import GameScreen

class MenuScreen():

    def __init__(self):
        self._ui_manager = UIManager(g.SCREEN_SIZE, "config/ui_theme.json")
        self._image = pygame.image.load("resources/full_canopy.png")
        self.menu = MainMenu(self._ui_manager)
        

    def process_event(self, event):
        screen_transition = None
        if event.type == pygame.KEYDOWN:
            self.menu.handle_keydown(event.key)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            command = self.menu.handle_button_pressed(event)
            if command.menu_option == MenuOption.MAIN_CONTINUE:
                if command.transition_type == TransitionType.BARN_DOOR_TRANSITION:
                    transition = BarnDoorTransition(pygame.image.load("resources/left_canopy.png"),
                                                    pygame.image.load("resources/right_canopy.png"),
                                                    1, 1, 1)
                elif command.transition_type == TransitionType.RISING_FLOOD_TRANSITION:
                    peaks = [(9,9),   (11,12), (18,14), (20,17), (22,9),  (18,40), (22,41), 
                             (27,42), (31,43), (33,42), (38,18), (40,21), (41,24), (45,28), 
                             (50,30), (54,32), (57,32), (63,34), (67,34), (73,35), (67,44), 
                             (83,40), (93,45), (82,29), (87,22), (86,18), (64,10), (67,9), 
                             (70,8),  (72,7),  (75,6),  (79,5),  (82,5)]
                    transition = RisingFloodTransition(self._image, peaks, 100, 50)
                screen_transition = ScreenTransition(GameScreen(), transition)

        self._ui_manager.process_events(event)

        return screen_transition


    def update(self, time_delta, audio):
        self._ui_manager.update(time_delta / 1000.0)


    def draw(self, surface):
        surface.blit(self._image, self._image.get_rect())
        self._ui_manager.draw_ui(surface)
        