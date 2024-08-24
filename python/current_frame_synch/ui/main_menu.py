import sys
import pygame
import pygame_gui
from enum import Enum

import globals as g
from enums import MenuOption, TransitionType
from ui.menu import Menu, MenuCommand
from ui.game_screen import GameScreen
from ui.barn_door_transition import BarnDoorTransition


class MainMenu(Menu):

    def __init__(self, ui_manager):
        super().__init__(ui_manager, 
                         {"Continue":self._on_continue, 
                          "New Game":self._on_new_game, 
                          "Options":self._on_options, 
                          "Exit":self._on_exit}, 
                          top=150, 
                          left=80)


    def _on_continue(self):
        g.log(3, f"MainMenu._on_continue:")
        return MenuCommand(MenuOption.MAIN_CONTINUE, TransitionType.RISING_FLOOD_TRANSITION)


    def _on_new_game(self):
        g.log(3, f"MainMenu._on_new_game:")
        return MenuCommand(MenuOption.MAIN_CONTINUE, TransitionType.RISING_FLOOD_TRANSITION)


    def _on_options(self):
        g.log(3, f"MainMenu._on_options:")


    def _on_exit(self):
        g.log(3, f"MainMenu._on_exit:")
        pygame.quit()
        sys.exit()
