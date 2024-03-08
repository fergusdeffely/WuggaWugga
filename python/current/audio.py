import pygame, sys
from globals import *


class Audio():
    _sounds = {}
    _channel = None

    def __init__(self):
        print('audio:')
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())

        sound = pygame.mixer.Sound("resources/onekick.wav")
        self._sounds["onekick"] = sound
        sound = pygame.mixer.Sound("resources/synthbass.ogg")
        self._sounds["synthbass"] = sound


    def _play_sound(self, name, maxtime=0):
        sound = self._sounds.get(name)

        if sound != None:
            self._channel = sound.play(maxtime=maxtime)
            log(2, f"{pygame.time.get_ticks()}:Audio._play_sound: on channel: {self._channel.id}")
            self._channel.set_endevent(CHANNEL_READY_EVENT)

        return self._channel.id


    def play_beat(self):
        return self._play_sound("onekick", 200)

    def play_bass(self):
        return self._play_sound("synthbass", 200)