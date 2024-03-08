import pygame
from globals import *
from timeline_logger import timeline_logger

class BeatBug(pygame.sprite.Sprite):

    current_id = 0

    def __init__(self, location, t0):
        super().__init__()

        self.id = BeatBug.current_id
        BeatBug.current_id += 1
        self.image = pygame.Surface((BEATBUG_SIZE, BEATBUG_SIZE))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.location = location
        self._bearing = 'B'
        self._centre_in_gridrect(self.location, True, True)
        self.t0 = t0
        self._speed = BEATBUG_SPEED
        self._checkpoint = self.rect.center


    def _centre_in_gridrect(self, location, h_centre, v_centre):  
        grid = grid_to_screen(location) 
        grid_left = x(grid)
        grid_top = y(grid)
        
        if h_centre == True:
            self.rect.x = grid_left + H_CENTER_BEATBUG
        if v_centre == True:
            self.rect.y = grid_top + V_CENTER_BEATBUG
        

    def adjust_for_pause(self, gap):
        self.t0 += gap

    
    def update(self, frame_ticks, level_data, emitters, audio):

        # movement first
        direction = get_direction_vector(self._bearing)
        
        # movement is based on the time since leaving the last reference position
        elapsed_time = frame_ticks - self.t0
        distance = elapsed_time * self._speed / 1000.0

        # update screen position (one of either the x or y will always be 0)
        self.rect.centerx = round(x(self._checkpoint) + direction.x * distance)
        self.rect.centery = round(y(self._checkpoint) + direction.y * distance)

        if LOG_BUG_MOVEMENT:
            timeline_logger.log(f"bug{self.id}:moved to:{self.rect.center}", frame_ticks)
        current_location = screen_to_grid(self.rect.center)

        # check if the bug has entered a new tile
        if self.location != current_location:
            self.location = current_location

            # have we entered a tile with a emitter?
            for emitter in emitters:
                if emitter.location == self.location and emitter.suspended == False:
                    emitter.play(audio)

        # TODO: optimise by adding else?

        # check if bearing is changing
        new_bearing = get_grid_cell_data(self.location)
        if self._bearing != new_bearing:
            # has the bug arrived back to the nest?
            if new_bearing == 'F':
                #despawn
                self.kill()
                return
          
            # the bearing on the tile the bug is now in is different from the current bearing, 
            # which means a direction change is going to happen... soon...
            # we wait to change direction until we've moved through the centre of the new tile
            centre = get_tile_rect(self.location).center            
            if ((self._bearing == 'N' and y(self.rect.center) <= y(centre))
              or (self._bearing == 'S' and y(self.rect.center) >= y(centre))
              or (self._bearing == 'W' and x(self.rect.center) <= x(centre))
              or (self._bearing == 'B' and x(self.rect.center) >= x(centre))
              or (self._bearing == 'E' and x(self.rect.center) >= x(centre))):
                if self._bearing != 'B':
                    timeline_logger.log(f"bug{self.id}: bearing: from:{self._bearing} to:{new_bearing} at: {self.rect.center} tile: {centre}", frame_ticks)
                self.change_bearing(frame_ticks, new_bearing, centre)
        
  
    def change_bearing(self, frame_ticks, new_bearing, tile_centre):
        if self._bearing != 'B':
            # realign on with existing spawn times
            rounded_frame_ticks = frame_ticks - frame_ticks % 500
            self.t0 = rounded_frame_ticks + self.t0 % 500
            timeline_logger.log(f"new t0:{self.t0}", frame_ticks)
            self._checkpoint = tile_centre
        self._bearing = new_bearing

        if self._bearing == 'N' or self._bearing == 'S':
            self._centre_in_gridrect(self.location, True, False)
        elif self._bearing == 'W' or self._bearing == 'E':
            self._centre_in_gridrect(self.location, False, True)
  
  
    def get_current_position():
        return (self.rect.x, self.rect.y)
  