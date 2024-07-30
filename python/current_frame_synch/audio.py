import pygame, sys
from globals import *


class Audio():
    _sounds = {}
    _channel = None

    def __init__(self):
        print('audio:')
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())

        self._sounds["onekick"] = pygame.mixer.Sound("resources/onekick.wav")
        self._sounds["synthbass"] = pygame.mixer.Sound("resources/synthbass.ogg")
        self._sounds["ride3"] = pygame.mixer.Sound("resources/ride3.ogg")
        self._sounds["syntom_1"] = pygame.mixer.Sound("resources/syntom_1.ogg")

    def play_sound(self, name, maxtime=0):
        sound = self._sounds.get(name)

        if sound != None:
            self._channel = sound.play(maxtime=maxtime)
            log(2, f"{pygame.time.get_ticks()}:Audio._play_sound: on channel: {self._channel.id}")
            self._channel.set_endevent(CHANNEL_READY_EVENT)

        return self._channel.id   