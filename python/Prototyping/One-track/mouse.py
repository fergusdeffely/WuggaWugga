import pygame
from globals import *


class Mouse(pygame.sprite.Sprite):
  
    def __init__(self):
        super().__init__()      

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)

      
    def update(self, session, level):
        position = pygame.mouse.get_pos()
        topleft = get_tile_topleft(position)

        # different grid square?
        if self.rect.topleft != topleft:
            self.rect.x = x(topleft)
            self.rect.y = y(topleft)

            # is there a currently selected assistant?
            if session.selected_assistant is not None:
                session.selected_assistant.update(self.rect.topleft)

                colour = session.selected_assistant.shadow_colour

                # change the assistant's colour if it's placeable at this location
                location = screen_to_grid(self.rect.topleft)
                if level.is_assistant_placeable(location, session.selected_assistant):
                    colour = session.selected_assistant.colour

                session.selected_assistant.redraw(colour)

            self.draw_cursor()
            

    def draw_cursor(self):
        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)
  