import pygame
from enum import Enum
from globals import *
from outlined_text import OutlinedText

class InfoText():

    def __init__(self, position, text, colour, outlined=False, outline_colour="white"):
        self.position = position
        self.text = text
        self.colour = "#ff0000"
        self.outlined = outlined
        self.font = pygame.font.Font("eight_bit_dragon.ttf", 10)
        if self.outlined:
            self.outlined_text = OutlinedText(text, 1, self.font, self.colour, outline_colour)


    def update(self, text=None):
        if text is not None:
            self.text = text


    def draw(self, surface):
        if self.outlined:
            text_surface = self.outlined_text.render(self.text)
        else:
            text_surface = self.font.render(self.text, False, self.colour)
        
        surface.blit(text_surface, self.position)


