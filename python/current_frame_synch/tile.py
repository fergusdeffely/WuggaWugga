import pygame
import globals as g
 
class Tile(pygame.sprite.Sprite):

    def __init__(self, location_text, grid_offset):
        super().__init__()

        self._parse_tile_config(location_text, grid_offset)

        self.image = pygame.Surface((g.TILE_SIZE, g.TILE_SIZE))
        self.image.fill("grey")
        self.rect = pygame.Rect(self.position[0], self.position[1], g.TILE_SIZE, g.TILE_SIZE)


    def _parse_tile_config(self, location_text, grid_offset):
        i = location_text.find(':')
        x = int(location_text[:i])
        y = int(location_text[i+1:])
        self.location = pygame.Vector2(x,y)
        self.position = g.grid_to_screen(self.location, grid_offset)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
