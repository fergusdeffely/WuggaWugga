import pygame
from globals import *
from timeline_logger import timeline_logger

class TimelineEvent():

    def __init__(self, start_cycle, on_run, loop=1, interval=FRAMES_PER_SECOND, tag="Unspecified"):
        self._iterations = 0
        self._trigger_at = start_cycle
        self._interval = interval  
        self._on_run = on_run
        self.loop = loop
        self.tag = tag
        log(3, f"TimelineEvent {tag}: initialised at {start_cycle}")


    def is_due(self, cycle):
        if cycle >= self._trigger_at:
            return True
        else:
            return False


    def unpause(self, pause_cycles):
        self._trigger_at += pause_cycles


    def run(self):        
        self._on_run()
        self._iterations += 1
        
        log(4, f"TimelineEvent {self.tag}: run at: {self._trigger_at} next at: {self._trigger_at + self._interval}")
        # reschedule for next loop
        self._trigger_at += self._interval
