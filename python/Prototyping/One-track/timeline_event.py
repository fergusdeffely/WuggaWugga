import pygame
from globals import *

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


    def run(self):
        self._on_due()
        self._iterations += 1
        msg = "TimelineEvent: Rescheduling from to t={} to t={}"
        print (msg.format(self._t, self._t + self._interval))
        # reschedule for next loop
        self._t = self._t + self._interval
        
