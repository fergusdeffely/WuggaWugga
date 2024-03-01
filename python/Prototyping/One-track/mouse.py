import pygame
from globals import *


class MouseMode(Enum):
    SELECTION = 0
    PLACEMENT = 1


class Mouse(pygame.sprite.Sprite):
  
    def __init__(self):
        super().__init__()      

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.position = None
        self.mode = MouseMode.SELECTION
        self.draw_cursor()

      
    def update(self, session, level):
        position = pygame.mouse.get_pos()
        if position == self.position:
            # nothing to do if position hasn't changed
            return
        self.position = position

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
                if level.is_assistant_placeable(session.selected_assistant):
                    colour = session.selected_assistant.colour

                session.selected_assistant.redraw(colour)
            
            location = screen_to_grid(self.rect.center)
            show_cursor = level.check_for_mouseover(location)
            self.draw_cursor(show_cursor)


    def draw_cursor(self, show_cursor=True):
        self.image.fill("black")
        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        if show_cursor:
            pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)
