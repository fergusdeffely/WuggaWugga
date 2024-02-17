import pygame
from globals import *
from tracktile import TrackTile
from beatbug import BeatBug
from beater import Beater
from beater import BeaterType
from palette import Palette
from mouse import Mouse

class Level:

    def __init__(self, data, surface, audio):
        self.assistant_colour = None
        self.surface = surface
        self.audio = audio
        self.data = data
        self.initialise(data)

      
    def initialise(self, data):
        
        # add the tiles
        self.tiles = pygame.sprite.Group()
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell in ['N', 'S', 'W', 'E']:
                    tile = TrackTile((x, y), cell)
                    self.tiles.add(tile)
                elif cell == 'O':
                    self.spawner_location = (x, y)
              
        # create groups for the sprites
        self.bugs = pygame.sprite.Group()
        self.beaters = pygame.sprite.Group()

        # create the palette
        #self.palette = pygame.sprite.GroupSingle(Palette())
        self.palette = Palette()

        # create the mouse
        mouse = Mouse()
        self.mouse = pygame.sprite.GroupSingle(mouse)

  
    def draw(self):
        self.tiles.update()
        self.tiles.draw(self.surface)

        self.beaters.update()
        self.beaters.draw(self.surface)

        self.bugs.update(self.data, self.beaters, self.audio)
        self.bugs.draw(self.surface)

        self.palette.update()
        self.palette.draw(self.surface)

        self.mouse.update()
        self.mouse.draw(self.surface)
      

    def handle_click(self, event):

        location = screen_to_grid(event.pos)

        # check for palette option clicked
        new_colour = self.palette.handle_click(location=location)
        if new_colour is not None:
            self.palette.select([location, new_colour])

        # check for add beater
        cell = self.data[y(location)][x(location)]

        if(cell in "NSEW"):
            #TODO: Check if beater already exists in this location
            beater_type = None
            if self.palette.selected_colour() == "red":
                beater_type = BeaterType.KICK
            elif self.palette.selected_colour() == "yellow":
                beater_type = BeaterType.BASS
            
            if beater_type is not None:
                beater = Beater(location, self.palette.selected_colour(), beater_type)
                self.beaters.add(beater)

    
    def spawn_beatbug(self):
        if(self.spawner_location):
            bug = BeatBug(self.spawner_location)
            self.bugs.add(bug)