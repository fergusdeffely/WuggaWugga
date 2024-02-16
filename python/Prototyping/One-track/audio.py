import pygame, sys
from globals import *


class Audio():
    sounds = {}
    channel = None

    def __init__(self):
        print('audio:')
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())

        sound = pygame.mixer.Sound("onekick.wav")
        self.sounds["onekick"] = sound
        sound = pygame.mixer.Sound("synthbass.ogg")
        self.sounds["synthbass"] = sound


    def play_sound(self, name, maxtime=0):
        sound = self.sounds.get(name)
        if sound != None:
            if self.channel == None:
                self.channel = sound.play(maxtime=maxtime)
            elif self.channel.get_busy() == False:
                self.channel = sound.play(maxtime=maxtime)

    def play_beat(self):
        self.play_sound("onekick", 200)

    def play_bass(self):
        self.play_sound("synthbass", 200)