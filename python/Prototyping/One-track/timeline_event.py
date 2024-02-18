import pygame
from globals import *

class TimelineEvent():


    def __init__(self, start_time, on_due, loop=1, interval=1000):
        self.t = start_time
        self.loop = loop
        self.interval = interval
        self.iterations = 0
        self.on_due = on_due


    def is_due(self, current_time):
        if self.t <= current_time:
            return True
        else:
            return False


    def unpause(self, gap):
        self.t += gap


    def run(self):
        self.on_due()
        self.iterations += 1        
        print ("TimelineEvent: Rescheduling from to t={} to t={}".format(self.t, self.t + self.interval))
        # reschedule for next loop
        self.t = self.t + self.interval
        
