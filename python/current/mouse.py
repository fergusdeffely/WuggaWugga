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
        topleft = get_tile_topleft(pygame.mouse.get_pos())

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
            highlight = level.check_for_highlight(location)
            self.draw_cursor(highlight)


    def draw_cursor(self, highlight=False):
        self.image.fill("black")
        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        if highlight == False:
            pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)
