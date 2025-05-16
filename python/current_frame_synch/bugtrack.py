import pygame
import pygame_gui
import globals as g
from timeline_event import TimelineEvent
from tracktile import TrackTile
from beatbug import BeatBug

class BugTrack():

    def __init__(self, track_name, track_data, timeline, grid_offset):
        self.tiles = {}
        self._beatbugs = pygame.sprite.Group()

        self._parse_config(track_name, track_data, timeline, grid_offset)


    def _parse_config(self, track_name, track_data, timeline, grid_offset):
        # frequency, etc will eventually be specified in level json
        spawn_freq = track_data.get("beatbug_spawn_frequency", g.DEFAULT_BEATBUG_SPAWN_FREQ) * g.FRAMES_PER_SECOND
        spawn_beatbug_event = TimelineEvent(start_cycle=0, 
                                            on_run=self.spawn_beatbug, 
                                            loop=0,
                                            interval=spawn_freq,
                                            args={"grid_offset": grid_offset},
                                            tag=f"{track_name}: Spawn Beatbug Event")
        timeline.add_event(spawn_beatbug_event)

        self._bug_speed = track_data.get("beatbug_speed", g.DEFAULT_BEATBUG_SPEED)

        if track_data["tiles"]:
            for tile_location in track_data["tiles"].keys():
                tile = TrackTile(tile_location, track_data["tiles"][tile_location], grid_offset)

                if tile.info == 'F':
                    self._spawner_location = tile.location
                self.tiles[(tile.location.x, tile.location.y)] = tile


    def update(self, cycle, level, audio):
        for beatbug in self._beatbugs:
            beatbug.update(cycle, level, self, audio)
        

    def draw(self, surface):
        for tile in self.tiles.values():
            tile.draw(surface)


    def draw_beatbugs(self, surface):
        #self._beatbugs.draw(surface)

        for beatbug in self._beatbugs:
            beatbug.draw(surface)


    def get_exits(self, position, grid_offset):
        location = g.screen_to_grid(position, grid_offset)
        #print(f"get_exits: for location: {location}")

        # is the requested location one of the track tiles?
        for tile in self.tiles.values():
            if tile.location == location:
                return tile.exits
            
        return (0,0,0,0)


    def spawn_beatbug(self, args):
        if(self._spawner_location):
            grid_offset = args.get("grid_offset", 0)
            bug = BeatBug(self._spawner_location, grid_offset, self._bug_speed)
            self._beatbugs.add(bug)
