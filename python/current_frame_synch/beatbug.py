import pygame
from globals import *
from timeline_logger import timeline_logger

class BeatBug(pygame.sprite.Sprite):

    current_id = 0

    def __init__(self, location, level_offset):
        super().__init__()

        self.id = BeatBug.current_id
        BeatBug.current_id += 1
        self.image = pygame.Surface((BEATBUG_SIZE, BEATBUG_SIZE))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.location = location
        self.direction = VECTOR_EAST
        self._centre_in_gridrect(self.location, level_offset, True, True)
        self._speed = BEATBUG_SPEED
        self._just_spawned = True


    def _centre_in_gridrect(self, location, level_offset, h_centre, v_centre):  
        position = grid_to_screen(location, level_offset)
        
        if h_centre == True:
            self.rect.x = x(position) + H_CENTER_BEATBUG
        if v_centre == True:
            self.rect.y = y(position) + V_CENTER_BEATBUG

    
    def update(self, cycle, level, audio):

        # don't move on the cycle the bug spawns in
        if(self._just_spawned == True):
            timeline_logger.log(f"bug{self.id}: spawned at: {self.rect.center}", cycle)
            self._just_spawned = False
            return

        # update screen position (one of direction.x or direction.y will always be 0)
        self.rect.centerx = self.rect.centerx + self.direction.x
        self.rect.centery = self.rect.centery + self.direction.y
        
        if LOG_BUG_MOVEMENT:
            timeline_logger.log(f"bug{self.id}: moved to: {self.rect.center}", cycle)

        # check if the bug has entered a new tile
        current_location = screen_to_grid(self.rect.center, level.grid_offset)

        if self.location != current_location:
            self.location = current_location
            # have we entered a tile with a emitter?
            for emitter in level.emitters:
                if emitter.location == self.location and emitter.suspended == False:
                    emitter.play(audio)

        tile = level.tiles[(self.location.x, self.location.y)]        
        # is direction changing?
        new_direction = self.get_direction(tile, level)

        if new_direction != self.direction:
            # direction is changing
            timeline_logger.log(f"bug{self.id}: at:{tile.rect.center} from:{self.direction} to:{new_direction}", cycle)
            self.direction = new_direction
        

    def get_direction(self, tile, level):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit

        exit_info = level.get_exits(self.rect.center)
  
        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x >= x(tile.rect.center) * self.direction.x:
            # is this the end tile?
            if tile.info == "T":
                self.kill()

            # is there an exit in front?
            if self.direction.x == 1 and E(exit_info) == False:
                # try left, try right, then try reverse
                if N(exit_info): return VECTOR_NORTH
                elif S(exit_info): return VECTOR_SOUTH
                elif W(exit_info): return VECTOR_WEST
            if self.direction.x == -1 and W(exit_info) == 0:
                # try left, try right, then try reverse
                if S(exit_info): return VECTOR_SOUTH
                elif N(exit_info): return VECTOR_NORTH
                elif E(exit_info): return VECTOR_EAST

        if self.rect.centery * self.direction.y >= y(tile.rect.center) * self.direction.y:
            # is this the end tile
            if tile.info == "T":
                self.kill()
            
            # is there an exit in front?
            if self.direction.y == 1 and S(exit_info) == False:
                # try left, try right, then try reverse
                if E(exit_info): return VECTOR_EAST
                elif W(exit_info): return VECTOR_WEST
                elif N(exit_info): return VECTOR_NORTH
            if self.direction.y == -1 and N(exit_info) == 0:
                # try left, try right, then try reverse
                if W(exit_info): return VECTOR_WEST
                elif E(exit_info): return VECTOR_EAST
                elif S(exit_info): return VECTOR_SOUTH

        return self.direction
  
    def change_bearing(self, new_bearing, tile_centre):
        self._bearing = new_bearing

        if self._bearing == 'N' or self._bearing == 'S':
            self._centre_in_gridrect(self.location, True, False)
        elif self._bearing == 'W' or self._bearing == 'E':
            self._centre_in_gridrect(self.location, False, True)
    
    def get_current_position():
        return (self.rect.x, self.rect.y)
  