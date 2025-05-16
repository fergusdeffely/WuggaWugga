import pygame

import globals as g
from timeline_logger import timeline_logger
from spritesheet import SpriteSheet


class BeatBug(pygame.sprite.Sprite):

    current_id = 0

    def __init__(self, location, level_offset, speed=g.DEFAULT_BEATBUG_SPEED):
        super().__init__()

        self.id = BeatBug.current_id
        BeatBug.current_id += 1
        self._spritesheet = SpriteSheet("resources/dev_sprites/beatbug_chunk32.png", 0, 0, 4, 4, g.TILE_SIZE, g.TILE_SIZE)        

        self._register_animations()

        self.image = pygame.Surface((g.TILE_SIZE, g.TILE_SIZE))
        self.rect = self.image.get_rect()

        self.location = location
        self._speed = speed
        self.direction = g.VECTOR_EAST
        
        step = int(g.BEATBUG_ANIM_STEP / self._speed)
        self._spritesheet.play_animation("move_right", step=g.BEATBUG_ANIM_STEP)
        self._centre_in_gridrect(self.location, level_offset, True, True)
        
        self._just_spawned = True


    @property
    def hitbox(self):
        offset = (g.BEATBUG_SIZE - g.BEATBUG_HITBOX_SIZE) / 2
        return pygame.Rect(self.rect.left + offset, self.rect.top + offset, g.BEATBUG_HITBOX_SIZE, g.BEATBUG_HITBOX_SIZE)


    def _register_animations(self):        
        self._spritesheet.register_animation("move_up", [(0,0),(0,1),(0,2),(0,3)])
        self._spritesheet.register_animation("move_down", [(1,0),(1,1),(1,2),(1,3)])
        self._spritesheet.register_animation("move_left", [(2,0),(2,1),(2,2),(2,3)])
        self._spritesheet.register_animation("move_right", [(3,0),(3,1),(3,2),(3,3)])


    def _centre_in_gridrect(self, location, level_offset, h_centre, v_centre):        
        position = g.grid_to_screen(location, level_offset)
        
        if h_centre == True:
            self.rect.x = g.x(position) + g.H_CENTER_BEATBUG
        if v_centre == True:
            self.rect.y = g.y(position) + g.V_CENTER_BEATBUG

    
    def update(self, cycle, level, bugtrack, audio):

        # don't move on the cycle the bug spawns in
        if(self._just_spawned == True):
            timeline_logger.log(f"bug{self.id}: spawned at: {self.rect.center}", cycle)
            self._just_spawned = False
            return

        # update screen position (one of direction.x or direction.y will always be 0)
        self.rect.centerx = self.rect.centerx + self.direction.x * self._speed
        self.rect.centery = self.rect.centery + self.direction.y * self._speed
        
        if g.LOG_BUG_MOVEMENT:
            moveto = "moveto"
            if (self.rect.centerx % g.TILE_SIZE == int(g.TILE_SIZE/2) + 1 and 
                self.rect.centery % g.TILE_SIZE == int(g.TILE_SIZE/2) + 1):
                moveto = "MOVETO"

            timeline_logger.log(f"bug{self.id}: {moveto}: {self.rect.center}", cycle)

        # check if the bug has entered a new tile
        current_location = g.screen_to_grid(self.rect.center, level.grid_offset)

        if self.location != current_location:
            self.location = current_location

        tile = bugtrack.tiles[(self.location.x, self.location.y)]
        # is direction changing?
        new_direction = self.get_direction(tile, bugtrack, level.grid_offset)

        if new_direction != self.direction:
            # direction is changing
            timeline_logger.log(f"bug{self.id}: at:{tile.rect.center} from:{self.direction} to:{new_direction}", cycle)
            self._change_direction(new_direction)            

        self.image = self._spritesheet.update()

        # check for collisions with emitters
        for emitter in level.emitters:
            if emitter.playing() == False:
                if emitter.hitbox.colliderect(self.hitbox):
                    emitter.play(audio)


    def draw(self, surface):
        self._spritesheet.draw(surface, self.rect.left, self.rect.top)
        if g.DEBUG_SHOW_HITBOXES:
            pygame.draw.rect(surface, "yellow", self.hitbox)


    def _change_direction(self, new_direction):
        self.direction = new_direction
        if new_direction == g.VECTOR_NORTH:
            self._spritesheet.play_animation("move_up", step=g.BEATBUG_ANIM_STEP)
        elif new_direction == g.VECTOR_SOUTH:
            self._spritesheet.play_animation("move_down", step=g.BEATBUG_ANIM_STEP)
        elif new_direction == g.VECTOR_WEST:
            self._spritesheet.play_animation("move_left", step=g.BEATBUG_ANIM_STEP)
        elif new_direction == g.VECTOR_EAST:
            self._spritesheet.play_animation("move_right", step=g.BEATBUG_ANIM_STEP)


    def get_direction(self, tile, bugtrack, grid_offset):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit

        exit_info = bugtrack.get_exits(self.rect.center, grid_offset)
  
        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x >= g.x(tile.rect.center) * self.direction.x:
            # is this the end tile?
            if tile.info == "T":
                self.kill()

            # is there an exit in front?
            if self.direction.x == 1 and g.E(exit_info) == False:
                # try left, try right, then try reverse
                if g.N(exit_info): return g.VECTOR_NORTH
                elif g.S(exit_info): return g.VECTOR_SOUTH
                elif g.W(exit_info): return g.VECTOR_WEST
            if self.direction.x == -1 and g.W(exit_info) == 0:
                # try left, try right, then try reverse
                if g.S(exit_info): return g.VECTOR_SOUTH
                elif g.N(exit_info): return g.VECTOR_NORTH
                elif g.E(exit_info): return g.VECTOR_EAST

        if self.rect.centery * self.direction.y >= g.y(tile.rect.center) * self.direction.y:
            # is this the end tile
            if tile.info == "T":
                self.kill()
            
            # is there an exit in front?
            if self.direction.y == 1 and g.S(exit_info) == False:
                # try left, try right, then try reverse
                if g.E(exit_info): return g.VECTOR_EAST
                elif g.W(exit_info): return g.VECTOR_WEST
                elif g.N(exit_info): return g.VECTOR_NORTH
            if self.direction.y == -1 and g.N(exit_info) == 0:
                # try left, try right, then try reverse
                if g.W(exit_info): return g.VECTOR_WEST
                elif g.E(exit_info): return g.VECTOR_EAST
                elif g.S(exit_info): return g.VECTOR_SOUTH

        return self.direction
  

    def change_bearing(self, new_bearing, tile_centre):
        self._bearing = new_bearing

        if self._bearing == 'N' or self._bearing == 'S':
            self._centre_in_gridrect(self.location, True, False)
        elif self._bearing == 'W' or self._bearing == 'E':
            self._centre_in_gridrect(self.location, False, True)
    
    def get_current_position():
        return (self.rect.x, self.rect.y)
  