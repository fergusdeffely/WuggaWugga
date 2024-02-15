import pygame, sys
from globals import *


class Audio():
    sounds = {}
    channel = None

    def __init__(self):
        print('audio:')
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())

        filename = "./onekick.wav"
        sound = pygame.mixer.Sound(filename)
        print(f'{filename}: length = {sound.get_length()}')
        self.sounds["onekick"] = sound


    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound != None:
            if self.channel == None:
                self.channel = sound.play()
            elif self.channel.get_busy() == False:
                self.channel = sound.play()