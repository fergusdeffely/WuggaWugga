import pygame
from enum import Enum
from globals import *
from timeline_logger import timeline_logger

class Emitter(pygame.sprite.Sprite):

    _current_id = 0

    def __init__(self, frame_ticks, t0, emitter_type, location, position, speed):
        super().__init__()

        self.id = Emitter._current_id
        Emitter._current_id += 1
        self._type = emitter_type
        self.location = location
        self.direction = VECTOR_SOUTH
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.set_colorkey("black")
        self.colour = "#0000ff"
        self.colour_play = "#55aaff"
        self.colour_suspended = "#888888"
        self.rect = pygame.Rect(position, (TILE_SIZE, TILE_SIZE))

        self._t0 = t0
        self._speed = speed
        self._checkpoint = self.rect.center
        # suspend until we pass t0
        self.suspended = True
        self._suspended_at_t = frame_ticks
        self._suspend_for = t0 - frame_ticks
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
        if self._type == EmitterType.KICK:
            self.channel_id = audio.play_beat()
        elif self._type == EmitterType.BASS:
            self.channel_id = audio.play_bass()
        self.redraw()


    def suspend(self, frame_ticks, suspend_ticks):
        # suspend_ticks needs to be a multiple of 500 for this trick of 
        # adjusting t0 forward to work
        self._t0 += suspend_ticks
        suspend_action = None

        if self.suspended:
            suspend_action = SuspendAction.EXTENDED
            self._suspend_for += suspend_ticks
            timeline_logger.log(f"em{self.id}: add suspend:{suspend_ticks}: total sus:{self._suspend_for} new t0:{self._t0}", frame_ticks)
        else:
            self.suspended = True
            suspend_action = SuspendAction.ENTERED            
            self._suspended_at_t = frame_ticks
            self._suspend_for = suspend_ticks
            timeline_logger.log(f"em{self.id}: suspend: at:{self._suspended_at_t} for:{self._suspend_for}:  new t0:{self._t0}", frame_ticks)
        
        self.redraw()
        return suspend_action


    def adjust_for_pause(self, gap):
        self._t0 += gap
        if self.suspended:
            self._suspended_at_t += gap


    def get_info_text(self, frame_ticks):
        if self.suspended:
            ticks_remaining = self._suspended_at_t + self._suspend_for - frame_ticks
            return f"{ticks_remaining / 1000:.1f}"
        else:
            return None


    def update(self, frame_ticks, tiles, level_offset, beatbugs, audio):     
        if self.suspended == True:
            if self._suspended_at_t + self._suspend_for > frame_ticks:                
                timeline_logger.log(f"em{self.id}: suspended")
                return
            else:
                timeline_logger.log(f"em{self.id}: unsuspended: at:{self._suspended_at_t} for:{self._suspend_for}")
                self.suspended = False
                self.redraw()

        # movement is based on the time since leaving the last reference position
        elapsed_time = frame_ticks - self._t0
        distance = elapsed_time * self._speed / 1000.0

        # update screen position (one of either the x or y will always be 0)
        self.rect.centerx = round(self._checkpoint[0] + self.direction.x * distance)
        self.rect.centery = round(self._checkpoint[1] + self.direction.y * distance)
        timeline_logger.log(f"em{self.id}: t0:{self._t0} chk:{self._checkpoint} moveto: {self.rect.center}", frame_ticks)
        
        # has location changed?
        new_location = screen_to_grid(self.rect.center, level_offset)        
        if self.location != new_location:
            self.location = new_location
            # have we happened upon a bug?
            for beatbug in beatbugs:
                if beatbug.location == self.location:
                    self.play(audio)
        
        tile_rect = get_tile_rect(self.location, level_offset)

        # is direction changing?
        new_direction = self.get_direction(tile_rect, level_offset)

        if new_direction != self.direction:
            # direction is changing, so update the checkpoint and t0
            #  - ensure new t0 keeps a granularity of 500ms with existing
            rounded_frame_ticks = frame_ticks - frame_ticks % 500
            self._t0 = rounded_frame_ticks + self._t0 % 500
            timeline_logger.log(f"em{self.id}: from:{self.direction} to:{new_direction} chk:{tile_rect.center}, t0:{self._t0}", frame_ticks)
            self._checkpoint = tile_rect.center
            self.direction = new_direction


    def get_direction(self, tile_rect, level_offset):
        # if we are past the centre of the current tile and
        # the exit in the current direction is not open,
        # find an available exit

        exit_info = self.assistant.get_exits(self.rect.center, level_offset)

        # Note:
        # take a sample x-axis (o = origin)
        #
        # .....-x2....-x1.....o.....x1....x2.....
        #
        #  x2 > x1
        # -x1 > -x2

        if self.rect.centerx * self.direction.x >= x(tile_rect.center) * self.direction.x:    
            # try left, try right, then try reverse
            if self.direction.x == 1 and E(exit_info) == False:
                if N(exit_info): return VECTOR_NORTH
                elif S(exit_info): return VECTOR_SOUTH
                elif W(exit_info): return VECTOR_WEST
            if self.direction.x == -1 and W(exit_info) == 0:
                if S(exit_info): return VECTOR_SOUTH
                elif N(exit_info): return VECTOR_NORTH
                elif E(exit_info): return VECTOR_EAST

        if self.rect.centery * self.direction.y >= y(tile_rect.center) * self.direction.y:
            if self.direction.y == 1 and S(exit_info) == False:
                if E(exit_info): return VECTOR_EAST
                elif W(exit_info): return VECTOR_WEST
                elif N(exit_info): return VECTOR_NORTH
            if self.direction.y == -1 and N(exit_info) == 0:
                if W(exit_info): return VECTOR_WEST
                elif E(exit_info): return VECTOR_EAST
                elif S(exit_info): return VECTOR_SOUTH

        return self.direction
            
