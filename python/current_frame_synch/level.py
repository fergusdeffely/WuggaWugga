import pygame
import copy
import json
from globals import *
from timeline_logger import timeline_logger
from timeline import Timeline
from timeline_event import TimelineEvent
from tracktile import TrackTile
from assistant import Assistant
from beatbug import BeatBug
from emitter import Emitter
from mouse import MouseMode
from info_text import InfoText
from info_text import SpriteInfoText
from bugtrack import BugTrack

class LevelRunState(Enum):
    INITIALISING = 0
    RUNNING = 1
    PAUSED = 2
    PLAY_TUNE = 3


class Level():

    def __init__(self, level_filename):
        self.runstate = LevelRunState.INITIALISING
        self._assistants = pygame.sprite.Group()
        self._bugtracks = []
        self.emitters = pygame.sprite.Group()
        self._sprite_infos = []
        self.assistant_roster = []
        self.selected_assistant = None
        self._timeline = Timeline()
        
        with open(level_filename) as f:
            d = json.load(f)
            self._parse_config(d)
        

    def _parse_config(self, data):

        log(4, f"level data:\n{data}")
        self.width = data["width"]
        self.height = data["height"]

        self.grid_offset = pygame.Vector2((SCREEN_WIDTH_TILES - self.width) / 2, 
                                          (SCREEN_HEIGHT_TILES - self.height) / 2)

        print(f"level: grid_offset: {self.grid_offset}")

        # create the assistant roster
        # TODO: move parse logic into Assistant
        for assistant_name in data["assistants"].keys():
            assistant_type = self._parse_assistant_type(data["assistants"][assistant_name]["type"])
            emit_sound = data["assistants"][assistant_name]["emit_sound"]
            play_duration = data["assistants"][assistant_name]["play_duration"]
            colour = pygame.Color(data["assistants"][assistant_name]["colour"])
            shadow_colour = pygame.Color(data["assistants"][assistant_name]["shadow_colour"])
            # lower the alpha for the shadow colour
            shadow_colour[3] = 150
            speed = data["assistants"][assistant_name]["speed"]
            nodes = {}
            for location_text, exits in data["assistants"][assistant_name]["nodes"].items():
                i = location_text.find(':')
                x = int(location_text[:i])
                y = int(location_text[i+1:])
                nodes[(x, y)] = exits

            assistant = Assistant(assistant_type, emit_sound, play_duration, nodes, colour, shadow_colour, speed)
            self.assistant_roster.append(assistant)

        # add the tracks
        for track_name in data["tracks"].keys():
            self._bugtracks.append(BugTrack(track_name, 
                                            data["tracks"][track_name], 
                                            self._timeline, 
                                            self.grid_offset))

        self.runstate = LevelRunState.RUNNING


    def _parse_assistant_type(self, type_string):
        if type_string == "path":
            return AssistantType.PATH


    def play_tune(self, cycle, name):
        self.runstate = LevelRunState.PLAY_TUNE
        track = {32:"onekick", 64:"onekick", 96:"synthbass", 128:"onekick"}
        self.tune = Tune([track])
        self.tune.play(cycle)


    def update(self, cycle, audio):
        self._timeline.update(cycle)
        
        if self.runstate == LevelRunState.RUNNING:
            # update emitters first
            self.emitters.update(cycle, self.grid_offset)
            # note: track updates move bugs and check for collisions
            for bugtrack in self._bugtracks:
                bugtrack.update(cycle, self, audio)
            for sprite_info in list(self._sprite_infos):
                if sprite_info.update(cycle) == False:
                    self._sprite_infos.remove(sprite_info)
        elif self.runstate == LevelRunState.PLAY_TUNE:
            self.tune.play_at(cycle)
                

    def draw(self, surface):
        if DRAW_GRID == True:
            self.draw_grid(surface)
        for bugtrack in self._bugtracks:
            bugtrack.draw(surface)
        self._assistants.draw(surface)
        self.emitters.draw(surface)
        for bugtrack in self._bugtracks:
            bugtrack.draw_beatbugs(surface)
        for sprite_info_text in self._sprite_infos:
            sprite_info_text.draw(surface)


    def pause(self):
        self.runstate = LevelRunState.PAUSED
        self._timeline.pause()


    def unpause(self, paused_cycles):
        self.runstate = LevelRunState.RUNNING        

        for emitter in self.emitters:
            emitter.adjust_for_pause(paused_cycles)

        self._timeline.unpause(paused_cycles)


    def draw_grid(self, surface):
        # vertical lines
        for x in range(self.width + 1):
            pygame.draw.line(surface, "#75757575", 
                             ((x + self.grid_offset.x)*TILE_SIZE, self.grid_offset.y * TILE_SIZE),
                             ((x + self.grid_offset.x)*TILE_SIZE, (self.height + self.grid_offset.y)* TILE_SIZE))

        # horiztonal lines
        for y in range(self.height + 1):
            pygame.draw.line(surface, "#75757575", 
                             (self.grid_offset.x * TILE_SIZE, (y + self.grid_offset.y)*TILE_SIZE), 
                             ((self.width + self.grid_offset.x)* TILE_SIZE, (y + self.grid_offset.y)*TILE_SIZE))


    def handle_click_button1(self, cycle, event_pos, mouse):
        if mouse.mode == MouseMode.SELECTION:
            location = screen_to_grid(event_pos, self.grid_offset)
            anchored_assistant = self.assistant_at(location)
            # if an assistant has been clicked, suspend the emitter
            if anchored_assistant:
                # but don't suspend emitters that are currently playing sounds
                if anchored_assistant.emitter.play_counter <= 0:
                    suspend_action = anchored_assistant.emitter.suspend(cycle, SUSPEND_FRAMES)
                    if suspend_action == SuspendAction.SUSPENDED:
                        countdown_text = SpriteInfoText(anchored_assistant.emitter, 
                                                        INFO_TEXT_OFFSET,
                                                        None, "#333333", True, "#cccccc", True)
                        self._sprite_infos.append(countdown_text)
            return

        if self.selected_assistant == None:
            return

        if self.is_assistant_placeable(self.selected_assistant):
            # add a new assistant to the level
            location = screen_to_grid(event_pos, self.grid_offset)
            # set the assistant into the level
            assistant = copy.deepcopy(self.selected_assistant)
            assistant.anchored = True
            # create an emitter

            synch_cycle = get_synchronised_cycle(cycle, assistant.speed)

            emitter = Emitter(synch_cycle,
                              assistant.emit_sound,
                              assistant.play_duration,
                              location,
                              get_tile_rect(location, self.grid_offset).topleft,
                              assistant.speed)
            emitter.assistant = assistant
            assistant.emitter = emitter
            # emitter will initially be suspended to synch with track timing
            # display the suspend time on screen
            countdown_text = SpriteInfoText(emitter, INFO_TEXT_OFFSET,
                                            None, "#333333", True, "#cccccc", True)
            self._sprite_infos.append(countdown_text)                                            
            timeline_logger.log(f"em{emitter.id} create at: {emitter.rect.center} synch at: {synch_cycle}", cycle)

            self._assistants.add(assistant)
            self.emitters.add(emitter)

            mouse.mode = MouseMode.SELECTION
            self.selected_assistant = None


    def handle_click_button2(self, cycle, position, mouse):
        # if in selection mode, second mouse button removes a placed assistant
        # and moves that assistant to placement mode
        if mouse.mode == MouseMode.SELECTION:            
            location = screen_to_grid(position, self.grid_offset)
            anchored_assistant = self.assistant_at(location)
            if anchored_assistant:
                # remove any associated info text            
                for sprite_info in list(self._sprite_infos):
                    if sprite_info.has_sprite(anchored_assistant.emitter):
                        self._sprite_infos.remove(sprite_info)
                # detach the assistant
                self.emitters.remove(anchored_assistant.emitter)
                self._assistants.remove(anchored_assistant)
                self.selected_assistant = anchored_assistant
                self.selected_assistant.anchored = False

                mouse.mode = MouseMode.PLACEMENT

        elif mouse.mode == MouseMode.PLACEMENT:
            if self.selected_assistant is not None:
                self.selected_assistant.rotate(self.grid_offset)
                if self.is_assistant_placeable(self.selected_assistant):
                    self.selected_assistant.redraw()
                else:
                    self.selected_assistant.redraw(self.selected_assistant.shadow_colour)                
                

    def assistant_at(self, location):
        for assistant in self._assistants.sprites():
            if assistant.has_node(location):
                return assistant

        return None


    def track_tile_at(self, location):
        tile = self.tiles.get((location.x, location.y))
        if tile is not None:
            # don't include start and finish tiles
            if tile.info != 'F' and tile.info != 'T':
                return True

        return False


    def is_assistant_placeable(self, assistant):
        locations = assistant.get_node_locations()
        track_tile_count = 0
        for location in locations:
            if x(location) < 0 or y(location) < 0:
                continue
            if x(location) >= self.width or y(location) >= self.height:
                continue
            # can't place over another assistant
            if self.assistant_at(location) is not None:
                return False
            
            for bugtrack in self._bugtracks:
                tile = bugtrack.tiles.get((location.x, location.y))
                if tile is not None:
                    if tile.info != 'F' and tile.info != 'T':
                        track_tile_count += 1

        if track_tile_count == 1:
            return True

        return False


    def on_new_mouse_location(self, location):
        # return is True if the mouse outline should be hidden

        assistant_at_location = self.assistant_at(location)
        
        for assistant in self._assistants:
            if assistant == assistant_at_location:
                assistant.highlight = True
            else:
                assistant.highlight = False
            assistant.redraw()

        if(location.x < 0 or location.x >= self.width or
           location.y < 0 or location.y >= self.height):
           return True

        return assistant_at_location is not None
