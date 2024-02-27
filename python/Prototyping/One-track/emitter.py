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


    def update(self, beatbugs, audio):

        self.check_for_direction_change()

        # update screen position
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y

        old_location = self.location
        self.location = screen_to_grid(self.rect.center)
        
        if self.location != old_location:
            # have we happened upon a bug?
            for beatbug in beatbugs:
                if beatbug.location == self.location:
                    self.play(audio)


    def check_for_direction_change(self):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit

        exit_info = self.assistant.get_exits(self.rect.center)

        centre = get_tile_rect(self.location).center

        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x > x(centre) * self.direction.x:
            # try left, try right, then try reverse
            if self.direction.x == 1 and E(exit_info) == False:
                if N(exit_info): self.direction = pygame.Vector2(0, -1)
                elif S(exit_info): self.direction = pygame.Vector2(0, 1)
                elif W(exit_info): self.direction = pygame.Vector2(-1, 0)
            if self.direction.x == -1 and W(exit_info) == 0:
                if S(exit_info): self.direction = pygame.Vector2(0, 1)
                elif N(exit_info): self.direction = pygame.Vector2(0, -1)
                elif E(exit_info): self.direction = pygame.Vector2(1, 0)

        if self.rect.centery * self.direction.y > y(centre) * self.direction.y:
            if self.direction.y == 1 and S(exit_info) == False:
                if E(exit_info): self.direction = pygame.Vector2(1, 0)
                elif W(exit_info): self.direction = pygame.Vector2(-1, 0)
                elif N(exit_info): self.direction = pygame.Vector2(0, -1)
            if self.direction.y == -1 and N(exit_info) == 0:
                if W(exit_info): self.direction = pygame.Vector2(-1, 0)
                elif E(exit_info): self.direction = pygame.Vector2(1, 0)
                elif S(exit_info): self.direction = pygame.Vector2(0, 1)
