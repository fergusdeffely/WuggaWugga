import pygame, sys
from gensound import WAV
from globals import *

class Audio():
    _sounds = {}

    def __init__(self):
        self._sounds["onekick"] = WAV("resources/onekick.wav")
        self._sounds["synthbass"] = WAV("resources/synthbass.wav")
        self._sounds["ride"] = WAV("resources/ride.wav")
        self._sounds["syntom"] = WAV("resources/syntom.wav")

    def play_sound(self, name):
        sound = self._sounds.get(name)

        if sound != None:
            sound.play()
        else:
            log(3, "Audio.play_sound: sound not found: {name}")