import pygame
from globals import *

class BeatBug(pygame.sprite.Sprite):

  def __init__(self, spawner_location):
    super().__init__()

    self.image = pygame.Surface((BEATBUG_SIZE, BEATBUG_SIZE))
    self.image.fill("green")
    self.rect = self.image.get_rect()
    
    self.location = spawner_location
    # always start North for now...
    self.bearing = 'O'
    self.centre_in_gridrect(spawner_location, True, True)


  def centre_in_gridrect(self, location, h_centre, v_centre):  
    grid = grid_to_screen(location) 
    grid_left = x(grid)
    grid_top = y(grid)
    
    if h_centre == True:
      self.rect.x = grid_left + H_CENTER_BEATBUG
    if v_centre == True:
      self.rect.y = grid_top + V_CENTER_BEATBUG
      
    
  def update(self, level_data):
  
    # check if bearing is changing
    location = screen_to_grid(self.rect.center)
    new_bearing = get_grid_cell_data(location)
 
    if self.bearing != new_bearing:
      # has the bug arrived back to the nest?
      if new_bearing == 'O':
        #despawn
        self.kill()
        return
    
      # bearing is changing, but are we past the centre within the 
      # current tile where direction needs to change?
      if (self.bearing == 'N' and y(self.rect.center) < y(get_grid_rect(location).center)) \
        or (self.bearing == 'O' and y(self.rect.center) < y(get_grid_rect(location).center)) \
        or (self.bearing == 'S' and y(self.rect.center) > y(get_grid_rect(location).center)) \
        or (self.bearing == 'W' and x(self.rect.center) < x(get_grid_rect(location).center)) \
        or (self.bearing == 'E' and x(self.rect.center) > x(get_grid_rect(location).center)):
          self.change_bearing(new_bearing, location)
          
    # movement
    direction = get_direction_vector(self.bearing)
    
    # update screen position
    self.rect.x += direction.x
    self.rect.y += direction.y
      
  
  def change_bearing(self, new_bearing, location):
    self.bearing = new_bearing
    if self.bearing == 'N' or self.bearing == 'S':
      self.centre_in_gridrect(location, True, False)
    elif self.bearing == 'W' or self.bearing == 'E':
      self.centre_in_gridrect(location, False, True)
  
  def get_current_position():
    return (self.rect.x, self.rect.y)
  