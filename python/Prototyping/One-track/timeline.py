import pygame
from globals import *
from timeline_event import TimelineEvent


class Timeline():


    def __init__(self):
        self._paused = False
        self._timeline_events = []


    def add_event(self, event):
        self._timeline_events.append(event)


    def pause(self):
        self._paused = True
        self.paused_at = pygame.time.get_ticks()


    def unpause(self):
        self._paused = False
        gap = pygame.time.get_ticks() - self.paused_at
        print ("unpausing - gap = %s" % gap)
        for event in self._timeline_events:
            event.unpause(gap)


    def update(self):

        if self._paused == True:
            return

        cleanup = []

        t = pygame.time.get_ticks()
        
        # run timeline events which are due
        for event in self._timeline_events:
            if event.is_due(t):
                event.run()

                if event.loop != 0 and event.iterations >= event.loop:
                    cleanup.append(event)

        # cleanup completed timeline events
        for event in cleanup:
            self._timeline_events.remove(event)
