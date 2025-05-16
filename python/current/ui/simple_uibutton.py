import pygame
from pygame_gui.elements import UIButton

from globals import *

class SimpleUIButton(UIButton):

    def __init__(self, rect, text, manager, anchors, name):
        super().__init__(relative_rect=rect, text=text, manager=manager, anchors=anchors)
        self.name = name
