import pygame
from globals import *
from timeline_logger import timeline_logger

class BeatBug(pygame.sprite.Sprite):

    current_id = 0

    def __init__(self, location, level_offset, t0):
        super().__init__()

        self.id = BeatBug.current_id
        BeatBug.current_id += 1
        self.image = pygame.Surface((BEATBUG_SIZE, BEATBUG_SIZE))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.location = location
        self.direction = VECTOR_EAST
        self._centre_in_gridrect(self.location, level_offset, True, True)
        self.t0 = t0
        self._speed = BEATBUG_SPEED
        self._checkpoint = self.rect.center


    def _centre_in_gridrect(self, location, level_offset, h_centre, v_centre):  
        position = grid_to_screen(location, level_offset)
        
        if h_centre == True:
            self.rect.x = x(position) + H_CENTER_BEATBUG
        if v_centre == True:
            self.rect.y = y(position) + V_CENTER_BEATBUG
        

    def adjust_for_pause(self, gap, at_ticks):
        timeline_logger.log(f"bug{self.id}: unpause: old t0:{self.t0}: new t0:{self.t0 + gap}", at_ticks)
        self.t0 += gap

    
    def update(self, frame_ticks, level, audio):

        # movement is based on the time since leaving the last reference position
        elapsed_time = frame_ticks - self.t0
        distance = elapsed_time * self._speed / 1000.0

        # update screen position (one of either the x or y will always be 0)
        self.rect.centerx = round(x(self._checkpoint) + self.direction.x * distance)
        self.rect.centery = round(y(self._checkpoint) + self.direction.y * distance)

        if LOG_BUG_MOVEMENT:
            timeline_logger.log(f"bug{self.id}:moved to:{self.rect.center}", frame_ticks)

        # check if the bug has entered a new tile
        current_location = screen_to_grid(self.rect.center, level.grid_offset)

        if self.location != current_location:
            #print(f"bug{self.id}: new tile: {current_location}, prev: {self.location}")
            self.location = current_location
            # have we entered a tile with a emitter?
            for emitter in level.emitters:
                if emitter.location == self.location and emitter.suspended == False:
                    emitter.play(audio)

        tile = level.tiles[(self.location.x, self.location.y)]
        #print(f"bug{self.id}: centre:{self.rect.center}, location: {self.location}, tile_centre:{tile.rect.center}")
        # is direction changing?
        new_direction = self.get_direction(tile, level)

        if new_direction != self.direction:
            # direction is changing, so update the checkpoint and t0
            #  - ensure new t0 keeps a granularity of 500ms with existing
            rounded_frame_ticks = frame_ticks - frame_ticks % 500
            self.t0 = rounded_frame_ticks + self.t0 % 500
            timeline_logger.log(f"em{self.id}: from:{self.direction} to:{new_direction} chk:{tile.rect.center}, t0:{self.t0}", frame_ticks)
            self._checkpoint = tile.rect.center
            self.direction = new_direction
        

    def get_direction(self, tile, level):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit

        exit_info = level.get_exits(self.rect.center)
        #print(f"bug{self.id}: exit_info: {exit_info}")

        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x >= x(tile.rect.center) * self.direction.x:
            # is this the end tile
            if tile.info == "T":
                self.kill()

            # try left, try right, then try reverse
            if self.direction.x == 1 and E(exit_info) == False:
                if N(exit_info): return VECTOR_NORTH
                elif S(exit_info): return VECTOR_SOUTH
                elif W(exit_info): return VECTOR_WEST
            if self.direction.x == -1 and W(exit_info) == 0:
                if S(exit_info): return VECTOR_SOUTH
                elif N(exit_info): return VECTOR_NORTH
                elif E(exit_info): return VECTOR_EAST

        if self.rect.centery * self.direction.y >= y(tile.rect.center) * self.direction.y:
            # is this the end tile
            if tile.info == "T":
                self.kill()
            
            if self.direction.y == 1 and S(exit_info) == False:
                if E(exit_info): return VECTOR_EAST
                elif W(exit_info): return VECTOR_WEST
                elif N(exit_info): return VECTOR_NORTH
            if self.direction.y == -1 and N(exit_info) == 0:
                if W(exit_info): return VECTOR_WEST
                elif E(exit_info): return VECTOR_EAST
                elif S(exit_info): return VECTOR_SOUTH

        return self.direction        
  
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
  