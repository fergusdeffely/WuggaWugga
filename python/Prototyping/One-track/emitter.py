import pygame
from enum import Enum
from globals import *


class Emitter(pygame.sprite.Sprite):
    def __init__(self, emitter_type, location, colour):
        super().__init__()

        self._type = emitter_type
        self.location = location
        self.direction = pygame.Vector2(0,0)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey("black")

        position = grid_to_screen(location)
        self.rect = pygame.Rect(x(position), y(position), TILE_SIZE, TILE_SIZE)

        # draw emitter icon
        if self._type == EmitterType.KICK:
            pygame.draw.circle(self.image, "blue", (TILE_SIZE/2, TILE_SIZE/2), TILE_SIZE / 3)
        if self._type == EmitterType.BASS:
            pygame.draw.circle(self.image, "blue", (TILE_SIZE/2, TILE_SIZE/2), TILE_SIZE / 3)
            self.direction = pygame.Vector2(0,1)


    def play(self, audio):
        if self._type == EmitterType.KICK:
            audio.play_beat()
        elif self._type == EmitterType.BASS:
            audio.play_bass()


    def update(self):
        # check if the emitter has entered a new tile

        exits = self.assistant.get_exits(self.rect.center)

        print("Emitter.update - current exits = ", exits)

        # # if current_location != self.location:
        # #     # we've entered a new segment
        # #     self.location = current_location

        # if self.assistant is not None:
        #     exits = self.assistant.get_exits(self.location)
        #     if (self.direction.x == 1 and exits[0] == 1 or
        #         self.direction.x == -1 and exits[1] == 1 or
        #         self.direction.y == 1 and exits[2] == 1 or
        #         self.direction.y == -1 and exits[3] == 1):

        # movement
        # TODO: movement rules
        
        # update screen position
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        self.location = screen_to_grid(self.rect.center)