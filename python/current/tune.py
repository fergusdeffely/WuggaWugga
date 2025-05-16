import pygame
import globals as g

class Tune():

    def __init__(self, tracks):
        self.tracks = tracks

    def play(self, start_cycle):
        self.start_cycle = start_cycle

    def play_at(self, cycle, audio):
        # get the current cycle in reference to the start cycle
        cycle -= self.start_cycle
        for track in self.tracks:
            if cycle in track:
                audio.play_sound(track[cycle])
