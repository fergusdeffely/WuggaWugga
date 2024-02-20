import pygame
from globals import *

class BeatBug(pygame.sprite.Sprite):

    def __init__(self, location):
        super().__init__()

        self.image = pygame.Surface((BEATBUG_SIZE, BEATBUG_SIZE))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self._location = location
        self._bearing = 'B'
        self._centre_in_gridrect(self._location, True, True)


    def _centre_in_gridrect(self, location, h_centre, v_centre):  
        grid = grid_to_screen(location) 
        grid_left = x(grid)
        grid_top = y(grid)
        
        if h_centre == True:
            self.rect.x = grid_left + H_CENTER_BEATBUG
        if v_centre == True:
            self.rect.y = grid_top + V_CENTER_BEATBUG
        
    
    def update(self, level_data, beaters, audio):    
        # check if the bug has entered a new tile
        location = screen_to_grid(self.rect.center)
        if self._location != location:
            self._location = location

            # have we entered a tile with a beater?
            for beater in beaters:
                if beater.location == location:
                    beater.play(audio)

        # check if bearing is changing
        new_bearing = get_grid_cell_data(location)
        if self._bearing != new_bearing:
            # has the bug arrived back to the nest?
            if new_bearing == 'F':
                #despawn
                self.kill()
                return
          
            # the bearing on the tile the bug is now in is different from the current bearing, 
            # which means a direction change is going to happen... soon...
            # we wait to change direction until we've moved through the centre of the new tile
            if ((self._bearing == 'N' and y(self.rect.center) < y(get_grid_rect(location).center))
              or (self._bearing == 'S' and y(self.rect.center) > y(get_grid_rect(location).center))
              or (self._bearing == 'W' and x(self.rect.center) < x(get_grid_rect(location).center))
              or (self._bearing == 'B' and x(self.rect.center) > x(get_grid_rect(location).center))
              or (self._bearing == 'E' and x(self.rect.center) > x(get_grid_rect(location).center))):
                self.change_bearing(new_bearing, location)
              
        # movement
        direction = get_direction_vector(self._bearing)
        
        # update screen position
        self.rect.x += direction.x
        self.rect.y += direction.y
        self._location = location
        
  
    def change_bearing(self, new_bearing, location):
        self._bearing = new_bearing
        if self._bearing == 'N' or self._bearing == 'S':
            self._centre_in_gridrect(location, True, False)
        elif self._bearing == 'W' or self._bearing == 'E':
            self._centre_in_gridrect(location, False, True)
  
  
    def get_current_position():
        return (self.rect.x, self.rect.y)
  