import pygame
import pygame_gui
from pygame_gui.elements import UIButton

import globals as g
from ui.menu_uibutton import MenuUIButton


class MenuCommand():
    def __init__(self, screen, transition):
        self.screen = screen
        self.transition = transition

    def __repr__(self):
        return f"MenuCommand: screen = {self.screen}, transiton = {self.transition}"


class Menu():

    def __init__(self, ui_manager, options, top, left):
        self._ui_manager = ui_manager        
        self._menu_options = options
        self._selected_id = 0
        self._build_menu(top, left)

    @property
    def selected_button(self):
        return self._buttons[self._selected_id]


    def _build_menu(self, top, left):
        self._buttons = {}
        button_id = 0
        
        for text, on_pressed in self._menu_options.items():
            button = MenuUIButton(rect=pygame.Rect(left, top, g.MENU_BUTTON_WIDTH, g.MENU_BUTTON_HEIGHT),
                                  text=text,
                                  manager=self._ui_manager,
                                  id=button_id,
                                  on_pressed=on_pressed)
            self._buttons[button_id] = button
            if button_id == self._selected_id:
                button.select()
            
            button_id += 1
            top = top + g.MENU_BUTTON_HEIGHT + g.MENU_BUTTON_SEPARATOR


    def handle_button_pressed(self, event):
        # run the method corresponding to this option
        return event.ui_element.on_pressed()
        

    def handle_keydown(self, key):
        if key == pygame.K_UP:
            self.selected_button.unselect()
            if self._selected_id == 0:
                self._selected_id = len(self._buttons) - 1
            else:
                self._selected_id -= 1
            self.selected_button.select()
        elif key == pygame.K_DOWN:
            self.selected_button.unselect()
            self._selected_id += 1
            if self._selected_id >= len(self._buttons):
                self._selected_id = 0
            self.selected_button.select()
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            # pygame-gui doesn't support keyboard activation of buttons
            # workaround is to simulate a UI_BUTTON_PRESSED event
            event_data = {'ui_element': self._buttons[self._selected_id]}
            button_pressed_event = pygame.event.Event(pygame_gui.UI_BUTTON_PRESSED, event_data)
            pygame.event.post(button_pressed_event)
