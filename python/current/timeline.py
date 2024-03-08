import pygame
from globals import *
from timeline_event import TimelineEvent
from timeline_logger import timeline_logger

class Timeline():

    def __init__(self):
        self._paused = False
        self._event_queue = []


    def add_event(self, event):
        self._event_queue.append(event)


    def pause(self):
        self._paused = True


    def unpause(self, gap):
        for event in self._event_queue:
            event.unpause(gap)
        self._paused = False


    def update(self, frame_ticks):
        if self._paused == True:
            return

        cleanup = []
        
        # run timeline events which are due
        for event in self._event_queue:
            if event.is_due(frame_ticks):
                event.run(frame_ticks)

                if event.loop != 0 and event.iterations >= event.loop:
                    cleanup.append(event)

        # cleanup completed timeline events
        for event in cleanup:
            self._event_queue.remove(event)
