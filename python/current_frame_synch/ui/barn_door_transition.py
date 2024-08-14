from enum import Enum
import pygame
import pygame_gui
from pygame_gui.elements import UIButton

import globals as g
from ui.menu_uibutton import MenuUIButton

class TransitionState(Enum):
    CLOSING   = 0
    CLOSED    = 1
    OPENING   = 2
    COMPLETE  = 3


class BarnDoorTransition():
    def __init__(self, left_surface, right_surface, close_duration, wait_duration, open_duration):
        self.transitionState = TransitionState.CLOSING
        
        self._close_duration = int(close_duration * g.FRAMES_PER_SECOND)
        self._wait_duration = int(wait_duration * g.FRAMES_PER_SECOND)
        self._open_duration = int(open_duration * g.FRAMES_PER_SECOND)
        self._wait_frames = 0

        self._left_surface = left_surface        
        self._left_rect = self._left_surface.get_rect()
        # start off screen
        self._left_rect.left -= self._left_rect.width

        self._right_surface = right_surface
        self._right_rect = self._right_surface.get_rect()
        # start off screen
        self._right_rect.left = g.SCREEN_WIDTH_PIXELS


    def update(self):
        if self.transitionState == TransitionState.CLOSING:
            x_delta = g.SCREEN_WIDTH_PIXELS / (self._close_duration * 2)
            self._left_rect.left += x_delta
            self._right_rect.left -= x_delta
            if self._left_rect.right >= self._right_rect.left:
                self.transitionState = TransitionState.CLOSED
        elif self.transitionState == TransitionState.CLOSED:
            self._wait_frames += 1
            if self._wait_frames >= self._wait_duration:
                self.transitionState = TransitionState.OPENING
        elif self.transitionState == TransitionState.OPENING:
            x_delta = g.SCREEN_WIDTH_PIXELS / (self._open_duration * 2)
            self._left_rect.left -= x_delta
            self._right_rect.left += x_delta
            if self._left_rect.left + self._left_rect.width < 0:
                self.transitionState = TransitionState.COMPLETE


    def draw(self, surface):
        surface.blit(self._left_surface, self._left_rect)
        surface.blit(self._right_surface, self._right_rect)

