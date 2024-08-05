import pygame
from enum import Enum
import globals as g
from globals import *
from timeline_logger import timeline_logger

class Emitter(pygame.sprite.Sprite):

    _current_id = 0

    def __init__(self, synch_cycle, emit_sound, play_duration, location, position, speed):
        super().__init__()

        self.id = Emitter._current_id
        Emitter._current_id += 1
        self._sound = emit_sound
        self._play_duration = play_duration
        self.location = location
        self.direction = VECTOR_SOUTH
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey("black")
        self.colour = "#0000ff"
        self.colour_play = "#55aaff"
        self.colour_suspended = "#888888"
        self.rect = pygame.Rect(position, (TILE_SIZE, TILE_SIZE))

        self._x_fractional = 0.0
        self._y_fractional = 0.0

        self._speed = speed

        # suspend until we synch
        self.suspended = True
        self._suspend_until = synch_cycle        
        self.play_counter = 0

        self.redraw()


    @property
    def hitbox(self):
        offset = (self.rect.width - EMITTER_HITBOX_SIZE) / 2
        return pygame.Rect(self.rect.left + offset, self.rect.top + offset, EMITTER_HITBOX_SIZE, EMITTER_HITBOX_SIZE)


    def redraw(self):
        # draw emitter icon
        if self.suspended:
            colour = self.colour_suspended
        elif self.play_counter > 0:
            colour = self.colour_play
        else:
            colour = self.colour

        centre_offset = int(TILE_SIZE/2)
        pygame.draw.circle(self.image, colour, (centre_offset, centre_offset), EMITTER_RADIUS)
        if g.DEBUG_SHOW_HITBOXES:
            hitbox_offset = (self.rect.width - EMITTER_HITBOX_SIZE) / 2
            hitbox_rect = pygame.Rect(hitbox_offset, hitbox_offset, EMITTER_HITBOX_SIZE, EMITTER_HITBOX_SIZE)
            pygame.draw.rect(self.image, "yellow", hitbox_rect)


    def play(self, audio):
        self.play_counter = self._play_duration
        audio.play_sound(self._sound)
        self.redraw()


    def playing(self):
        return self.play_counter > 0


    def suspend(self, cycle, num_cycles):
        suspend_action = None

        if self.suspended:
            self._suspend_until += num_cycles
            suspend_action = SuspendAction.EXTENDED
            timeline_logger.log(f"em{self.id}: suspend: extend by: {num_cycles} until:{self._suspend_until}", cycle)
        else:
            self._suspend_until = cycle + num_cycles - 1
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

    def update(self, cycle, level_offset):
        if self.play_counter > 0:
            self.play_counter -= 1
            if self.play_counter == 0:
                self.redraw()

        if self.suspended == True:
            if cycle < self._suspend_until :
                timeline_logger.log(f"em{self.id}: suspended", cycle)
                return
            else:
                timeline_logger.log(f"em{self.id}: unsuspended", cycle)
                self.suspended = False
                self.redraw()
                # don't move the turn suspend ends
                return

        exit_info = self.assistant.get_exits(self.rect.center, level_offset)

        if(N(exit_info) == False and S(exit_info) == False and E(exit_info) == False and W(exit_info) == False):
            # 1x1 assistant - no movement
            return

        # update screen position based on direction
        # note 1: one of direction.x or direction.y will always be 0
        # note 2: in the pygame.Rect type the center (x,y) is a tuple and is managed 
        #         as an integer pair - this means rounding of fractions
        #         storing fractional deltas for process when they reach a unit value
       
        x_fractional = self.direction.x * self._speed % 1
        x_delta = self.direction.x * self._speed - x_fractional

        self._x_fractional += x_fractional
        if self._x_fractional >= 1:
            self._x_fractional -= 1
            x_delta += 1

        y_fractional = self.direction.y * self._speed % 1
        y_delta = self.direction.y * self._speed - y_fractional

        self._y_fractional += y_fractional
        if self._y_fractional >= 1:
            self._y_fractional -= 1
            y_delta += 1

        self.rect.centerx += x_delta
        self.rect.centery += y_delta

        moveto = "moveto"
        if (self.rect.centerx % TILE_SIZE == int(TILE_SIZE/2) + 1 and 
            self.rect.centery % TILE_SIZE == int(TILE_SIZE/2) + 1):
            moveto = "MOVETO"

        timeline_logger.log(f"em{self.id}: {moveto}: {self.rect.center}", cycle)
        
        # different tile?
        new_location = screen_to_grid(self.rect.center, level_offset)
        if self.location != new_location:
            self.location = new_location

        # is direction changing?
        new_direction = self.get_direction(level_offset, exit_info)

        if new_direction != self.direction:
            # direction is changing
            timeline_logger.log(f"em{self.id}: from:{self.direction} to:{new_direction}", cycle)
            self.direction = new_direction


    def get_direction(self, level_offset, exit_info):
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

        current_tile_centre = g.get_tile_rect(self.location, level_offset).center

        if self.rect.centerx * self.direction.x >= x(current_tile_centre) * self.direction.x:
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

        if self.rect.centery * self.direction.y >= y(current_tile_centre) * self.direction.y:
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
            
