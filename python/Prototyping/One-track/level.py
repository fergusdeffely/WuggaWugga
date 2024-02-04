import pygame
from globals import *
from tracktile import TrackTile
from beatbug import BeatBug
from mouse import Mouse

class Level:

  def __init__(self, data, surface):
    self.display_surface = surface
    self.data = data
    self.initialise(data)

    
  def initialise(self, data):
    # add the tiles
    self.tiles = pygame.sprite.Group()
    for y, row in enumerate(data):
      for x, cell in enumerate(row):
        if cell in ['N', 'S', 'W', 'E']:
          tile = TrackTile((x, y), cell)
          self.tiles.add(tile)
        elif cell == 'O':
          self.spawner_location = (x, y)
          
    # create the bugs group
    self.bugs = pygame.sprite.Group()
      
    # create the mouse
    mouse = Mouse()
    self.mouse = pygame.sprite.GroupSingle(mouse)

  def spawn_beatbug(self):
    if(self.spawner_location):
      bug = BeatBug(self.spawner_location)
      self.bugs.add(bug)
  
  def draw(self):
    self.tiles.update()
    self.tiles.draw(self.display_surface)
    
    self.bugs.update(self.data)
    self.bugs.draw(self.display_surface)
    
    self.mouse.update()
    self.mouse.draw(self.display_surface)
    
  