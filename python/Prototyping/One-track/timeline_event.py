import pygame
from globals import *
from timeline_logger import timeline_logger

class TimelineEvent():


    def __init__(self, start_time, on_due, loop=1, interval=1000):
        self._iterations = 0
        self._t = start_time        
        self._interval = interval        
        self._on_due = on_due
        self.loop = loop


    def is_due(self, current_time):
        if self._t <= current_time:
            return True
        else:
            return False


    def unpause(self, gap):
        self._t += gap


    def run(self, frame_ticks):
        timeline_logger.log(f"running timeline event due at {self._t}", frame_ticks)
        self._on_due(self._t, frame_ticks)
        self._iterations += 1
        msg = "TimelineEvent: frame={}: Rescheduling from to t={} to t={}"
        log(4, msg.format(frame_ticks, self._t, self._t + self._interval))

        
        # reschedule for next loop
        self._t = self._t + self._interval
        
