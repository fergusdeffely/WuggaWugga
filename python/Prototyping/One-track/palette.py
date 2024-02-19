import pygame
from globals import *

class Palette(pygame.sprite.Sprite):

    _assistants = {}                # location: colour
    _selected_assistant = None

    def __init__(self):
        super().__init__()

        print("Palette: Assistant list: ", ASSISTANT_LIST)

        # height for each option plus space between
        height = len(ASSISTANT_LIST) * 2
        self.image = pygame.Surface(grid_to_screen((2, height)), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        # build the assistants
        for i, colour in enumerate(ASSISTANT_LIST):
            location = (1, 1 + i*2)
            self._assistants[location] = colour


    def handle_click(self, location):
        return self._assistants.get(location)


    def draw(self, surface):
        for location, colour in self._assistants.items():
            rect = pygame.Rect(grid_to_screen(location), (TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.image, colour, rect)
            # highlighting
            if location == self.selected_location():
                pygame.draw.rect(self.image, "white", rect, 3)

        surface.blit(self.image, self.image.get_rect())


    def update(self):
        #TODO update status of palette options based on availability
        pass


    def select(self, assistant):
        print("Assistant selected: ", assistant)
        self._selected_assistant = assistant


    def selected(self):
        return self._selected_assistant


    def selected_location(self):
        if self._selected_assistant == None:
            return None
        else:
            return self._selected_assistant[0]

    
    def selected_colour(self):
        if self._selected_assistant == None:
            return None
        else:
            return self._selected_assistant[1]



    