import pygame
from pygame_gui.elements import UIButton

import globals as g

class MenuUIButton(UIButton):

    def __init__(self, rect, text, manager, id, on_pressed):
        super().__init__(relative_rect=rect, text=text, manager=manager)
        self.id = id
        self.on_pressed = on_pressed
