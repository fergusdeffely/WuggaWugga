import pygame
from globals import *

# Button code thanks to article by Maxim Maeder:
# https://thepythoncode.com/article/make-a-button-using-pygame-in-python


class Button():
    def __init__(self, x, y, width, height, text='Button', onclickFunction=None, onePress=False):
        self._font = pygame.font.SysFont('Courier New', 20)
        self._onclickFunction = onclickFunction
        self._onePress = onePress
        self._alreadyPressed = False

        self._fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self._buttonSurface = pygame.Surface((width, height))
        self._buttonRect = pygame.Rect(x, y, width, height)
        self._buttonText = self._font.render(text, True, (20, 20, 20))


    def draw(self, surface):
        mousePos = pygame.mouse.get_pos()
        self._buttonSurface.fill(self._fillColors['normal'])
        if self._buttonRect.collidepoint(mousePos):
            self._buttonSurface.fill(self._fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self._buttonSurface.fill(self._fillColors['pressed'])
                if self._onePress:
                    self._onclickFunction()
                elif not self._alreadyPressed:
                    self._onclickFunction()
                    self._alreadyPressed = True
            else:
                self._alreadyPressed = False        

        # blit the text
        self._buttonSurface.blit(self._buttonText, [
            self._buttonRect.width/2 - self._buttonText.get_rect().width/2,
            self._buttonRect.height/2 - self._buttonText.get_rect().height/2
            ])

        surface.blit(self._buttonSurface, self._buttonRect)