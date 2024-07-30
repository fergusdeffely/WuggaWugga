import pygame
from enum import Enum
from globals import *
from timeline_logger import timeline_logger

class Emitter(pygame.sprite.Sprite):

    _current_id = 0

    def __init__(self, synch_cycle, emit_sound, location, position, speed):
        super().__init__()

        self.id = Emitter._current_id
        Emitter._current_id += 1
        self._sound = emit_sound
        self.location = location
        self.direction = VECTOR_SOUTH
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey("black")
        self.colour = "#0000ff"
        self.colour_play = "#55aaff"
        self.colour_suspended = "#888888"
        self.rect = pygame.Rect(position, (TILE_SIZE, TILE_SIZE))

        self._x_delta = 0
        self._y_delta = 0

        self._speed = speed

        # suspend until we synch
        self.suspended = True
        self._suspend_until = synch_cycle        
        self.channel_id = None

        self.redraw()


    def redraw(self):
        # draw emitter icon
        colour = self.colour
        if self.suspended:
            colour = self.colour_suspended
        elif self.channel_id is not None:
            colour = self.colour_play

        pygame.draw.circle(self.image, colour, (TILE_SIZE/2, TILE_SIZE/2), TILE_SIZE / 3)


    def play(self, audio):
        self.channel_id = audio.play_sound(self._sound, 200)
        self.redraw()


    def suspend(self, cycle, num_cycles):
        suspend_action = None

        if self.suspended:
            self._suspend_until += num_cycles
            suspend_action = SuspendAction.EXTENDED
            timeline_logger.log(f"em{self.id}: suspend: extend by: {num_cycles} until:{self._suspend_until}", cycle)
        else:
            self._suspend_until = cycle + num_cycles
            self.suspended = True
            suspend_action = SuspendAction.SUSPENDED
            timeline_logger.log(f"em{self.id}: suspend: until:{self._suspend_until}", cycle)
        
        self.redraw()
        return suspend_action


    def adjust_for_pause(self, pause_cycles):
        if self.suspended:
            self._suspend_until += pause_cycles


    def get_info_text(self, cycle):
        if self.suspended:
            cycles_remaining = self._suspend_until - cycle
            return f"{cycles_remaining / FRAMES_PER_SECOND:.1f}"
        else:
            return None


    def update(self, cycle, tiles, level_offset, beatbugs, audio):     
        if self.suspended == True:
            if cycle < self._suspend_until :
                timeline_logger.log(f"em{self.id}: suspended", cycle)
                return
            else:
                timeline_logger.log(f"em{self.id}: unsuspended", cycle)
                self.suspended = False
                self.redraw()

        exit_info = self.assistant.get_exits(self.rect.center, level_offset)

        if(N(exit_info) == False and S(exit_info) == False and E(exit_info) == False and W(exit_info) == False):
            # 1x1 assistant - no movement
            return

        # update screen position based on direction
        # note 1: one of direction.x or direction.y will always be 0
        # note 2: in the pygame.Rect type the center (x,y) is a tuple and is managed 
        #         as an integer pair - this means rounding of fractions
        
        self._x_delta = self._x_delta + self.direction.x * 0.5
        if(self._x_delta >= 1):
            self._x_delta = self._x_delta - 1
            self.rect.centerx = self.rect.centerx + 1
        elif(self._x_delta <= -1):
            self._x_delta = self._x_delta + 1
            self.rect.centerx = self.rect.centerx - 1

        self._y_delta = self._y_delta + self.direction.y * 0.5
        if(self._y_delta >= 1):
            self._y_delta = self._y_delta - 1
            self.rect.centery = self.rect.centery + 1
        elif(self._y_delta <= -1):
            self._y_delta = self._y_delta + 1
            self.rect.centery = self.rect.centery - 1

        timeline_logger.log(f"em{self.id}: moveto: {self.rect.center}", cycle)
        
        # different tile?
        new_location = screen_to_grid(self.rect.center, level_offset)
        if self.location != new_location:
            self.location = new_location
            # have we happened upon a bug?
            for beatbug in beatbugs:
                if beatbug.location == self.location:
                    self.play(audio)
        
        tile_rect = get_tile_rect(self.location, level_offset)

        # is direction changing?
        new_direction = self.get_direction(tile_rect, level_offset, exit_info)

        if new_direction != self.direction:
            # direction is changing
            timeline_logger.log(f"em{self.id}: from:{self.direction} to:{new_direction}", cycle)
            self.direction = new_direction


    def get_direction(self, tile_rect, level_offset, exit_info):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit
        #
        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x >= x(tile_rect.center) * self.direction.x:
            
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

        if self.rect.centery * self.direction.y >= y(tile_rect.center) * self.direction.y:
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
            
