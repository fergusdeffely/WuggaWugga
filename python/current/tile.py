import pygame
import globals as g
 
class Tile(pygame.sprite.Sprite):

    def __init__(self, location_text):
        super().__init__()

        self._parse_tile_config(location_text)

        self.image = pygame.Surface((g.GRID_SIZE, g.GRID_SIZE))
        self.image.fill("grey")
        self.rect = pygame.Rect(self.position[0], self.position[1], g.GRID_SIZE, g.GRID_SIZE)


    def _parse_tile_config(self, location_text):
        i = location_text.find(':')
        x = int(location_text[:i])
        y = int(location_text[i+1:])
        self.location = pygame.Vector2(x,y)
        self.position = loc_to_pos(self.location)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
