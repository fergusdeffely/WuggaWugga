import pygame
from globals import *
from session import Session

class Mouse(pygame.sprite.Sprite):
  
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)

      
    def update(self, session):
        position = pygame.mouse.get_pos()
        grid = get_containing_grid(position)

        self.rect.x = x(grid)
        self.rect.y = y(grid)
        

    def redraw_mouse_pointer(self, session, level, location):
        assistant = session.selected_assistant
        frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))

        if assistant == None:
            pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)
        else:
            colour = assistant.shadow_colour
            
            # can the assistant be placed at this location?
            if level.is_assistant_placeable(location, assistant):
                colour = assistant.colour
            else:    
                # lower the alpha
                colour = assistant.shadow_colour

            pygame.draw.rect(self.image, colour, frame, border_radius=3)
            pygame.draw.rect(self.image, "#00ff0077", self.rect, 3, border_radius=3)
  

  