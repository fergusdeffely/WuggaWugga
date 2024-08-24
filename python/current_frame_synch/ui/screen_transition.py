import pygame
import pygame_gui

import globals as g


class ScreenTransition():
    def __init__(self, screen, transition=None):
        self.screen = screen
        self.transition = transition

    def __repr__(self):
        return f"ScreenTransition: screen = {self.screen}, transition = {self.transition}"