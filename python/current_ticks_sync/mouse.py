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

      
    def update(self, level):
        topleft = get_tile_topleft(pygame.mouse.get_pos())

        # different grid square?
        if self.rect.topleft != topleft:
            self.rect.x = x(topleft)
            self.rect.y = y(topleft)

            # is there a currently selected assistant?
            if level.selected_assistant is not None:
                # update it with the new mouse position
                level.selected_assistant.update(self.rect.topleft, level.grid_offset)

                # work out the colour depending on whether it's placeable
                colour = level.selected_assistant.shadow_colour                
                if level.is_assistant_placeable(level.selected_assistant):
                    colour = level.selected_assistant.colour

                print(f"mouse: redraw => colour:{colour}")
                level.selected_assistant.redraw(colour)
            
            # check to see if an anchored assistant is being highlighted
            highlight = level.check_for_highlight(screen_to_grid(self.rect.topleft, level.grid_offset))
            self.draw_cursor(highlight)


    def draw_cursor(self, highlight=False):
        self.image.fill("black")
        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        if highlight == False:
            pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
