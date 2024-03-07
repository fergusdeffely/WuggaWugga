import pygame
from enum import Enum
from globals import *
from outlined_text import OutlinedText


class InfoText():

    def __init__(self, position, text, colour, outlined=False, outline_colour="white"):
        self.position = position
        self.text = text
        self._colour = colour
        self.outlined = outlined
        self._font = pygame.font.Font("eight_bit_dragon.ttf", 10)        
        if self.outlined:
            self.outlined_text = OutlinedText(text, 1, self._font, self._colour, outline_colour)


    def update(self, position, text=None):
        self.position = position
        if text is not None:
            self.text = text


    def draw(self, surface):
        if self.outlined:
            self._text_surface = self.outlined_text.render(self.text)
        else:
            self._text_surface = self._font.render(self.text, False, self._colour)
        
        surface.blit(self._text_surface, self.position)


class SpriteInfoText():

    def __init__(self, sprite, offset, text, colour, outlined=False, outline_colour="white", centered=False):
        self._sprite = sprite
        self._offset = offset
        self.text = text
        self._colour = colour
        self._outlined = outlined
        self._font = pygame.font.Font("eight_bit_dragon.ttf", 10)        
        if self._outlined:
            self._outlined_text = OutlinedText(text, 1, self._font, self._colour, outline_colour)
        # text is position will be the sprite centre with the offset applied
        # if centered is true, the text will take this position as top centre
        # if centered is false, the text will take this position as topleft
        self._centered = centered

        # we render to allow for calculation of surface size and position
        self._rerender()


    def update(self, frame_ticks, text=None):
        text = self._sprite.get_info_text(frame_ticks)
        if text is None:
            return False
        
        if self.text != text:
            self.text = text
            # re-render to account for changed text
            if self._outlined:
                self._text_surface = self._outlined_text.render(self.text)
            else:
                self._text_surface = self._font.render(self.text, False, self._colour)

            # we render to allow for calculation of surface size and position
            self._rerender()
        
        return True


    def _rerender(self):
        if self._outlined:
            self._text_surface = self._outlined_text.render(self.text)
        else:
            self._text_surface = self._font.render(self.text, False, self._colour)

        self.position = self._sprite.rect.center + self._offset
        if self._centered:
             self.position = (x(self.position) - self._text_surface.get_width() / 2, y(self.position))


    def draw(self, surface):
        # surface has already been rendered
        self._text_surface.set_colorkey("black")
        surface.blit(self._text_surface, self.position)


    def has_sprite(self, sprite):
        return self._sprite == sprite
            