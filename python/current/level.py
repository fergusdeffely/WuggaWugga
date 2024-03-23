import pygame
import copy
import json
from globals import *
from timeline_logger import timeline_logger
from timeline_event import TimelineEvent
from tracktile import TrackTile
from assistant import Assistant
from beatbug import BeatBug
from emitter import Emitter
from mouse import MouseMode
from info_text import InfoText
from info_text import SpriteInfoText


class LevelRunState(Enum):
    INITIALISING = 0
    RUNNING = 1
    PAUSED = 2


class Level:

    def __init__(self, level_filename, out, session, t0):
        self.runstate = LevelRunState.INITIALISING
        self._out = out
        self.tiles = {}
        self._assistants = pygame.sprite.Group()
        self._bugs = pygame.sprite.Group()
        self.emitters = pygame.sprite.Group()
        self._sprite_infos = []
        self.assistant_roster = []
        self.selected_assistant = None
        
        with open(level_filename) as f:
            d = json.load(f)
            self._initialise(d)

        # frequency, etc will eventually be specified in level json
        spawn_beatbug_event = TimelineEvent(t0, self.spawn_beatbug, 0, BEATBUG_SPAWN_TIMER_DURATION)
        session.timeline.add_event(spawn_beatbug_event)
        

    def _initialise(self, data):

        log(4, f"level data:\n{data}")
        self.width = data["width"]
        self.height = data["height"]

        self.grid_offset = pygame.Vector2((SCREEN_WIDTH_TILES - self.width) / 2, 
                                          (SCREEN_HEIGHT_TILES - self.height) / 2)

        print(f"level: grid_offset: {self.grid_offset}")

        # create the assistant roster
        for assistant_name in data["assistants"].keys():
            assistant_type = self._parse_assistant_type(data["assistants"][assistant_name]["type"])
            emitter_type = self._parse_emitter_type(data["assistants"][assistant_name]["emitter"])
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

            assistant = Assistant(assistant_type, emitter_type, nodes, colour, shadow_colour, speed)
            self.assistant_roster.append(assistant)

        # add the tiles
        for location_text in data["tracks"].keys():
            i = location_text.find(':')
            x = int(location_text[:i])
            y = int(location_text[i+1:])
            location = pygame.Vector2(x,y)
            position = grid_to_screen(location, self.grid_offset)
            exits = data["tracks"][location_text]["exits"]
            info = data["tracks"][location_text].get("info")
            
            tile = TrackTile(location, position, exits, info)
            if info == 'F':
                self._spawner_location = pygame.Vector2(x, y)
            self.tiles[(x, y)] = tile

        self.runstate = LevelRunState.RUNNING
        print(self.tiles)


    def _parse_assistant_type(self, type_string):
        if type_string == "path":
            return AssistantType.PATH


    def _parse_emitter_type(self, type_string):
        if type_string == "kick":
            return EmitterType.KICK
        elif type_string == "bass":
            return EmitterType.BASS


    def update(self, frame_ticks, audio):
        if self.runstate == LevelRunState.RUNNING:
            # emitters need to know where bugs are and bugs need
            # to know where emitters are            
            self.emitters.update(frame_ticks, self.tiles, self.grid_offset, self._bugs, audio)
            self._bugs.update(frame_ticks, self, audio)
            for sprite_info in list(self._sprite_infos):
                if sprite_info.update(frame_ticks) == False:
                    self._sprite_infos.remove(sprite_info)
                

    def draw(self, surface):
        if DRAW_GRID == True:
            self.draw_grid(surface)
        for tile in self.tiles.values():
            tile.draw(surface)
        self._assistants.draw(surface)
        self.emitters.draw(surface)
        self._bugs.draw(surface)
        for sprite_info_text in self._sprite_infos:
            sprite_info_text.draw(surface)


    def pause(self):
        self.runstate = LevelRunState.PAUSED


    def unpause(self, gap, ticks):
        self.runstate = LevelRunState.RUNNING
        for bug in self._bugs:
            bug.adjust_for_pause(gap, ticks)

        for emitter in self.emitters:
            emitter.adjust_for_pause(gap)


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


    def get_exits(self, position):
        location = screen_to_grid(position, self.grid_offset)
        #print(f"get_exits: for location: {location}")

        # is the requested location one of the track tiles?
        for tile in self.tiles.values():
            if tile.location == location:
                return tile.exits
            
        return (0,0,0,0)


    def handle_click_button1(self, frame_ticks, event_pos, session, mouse):
        if mouse.mode == MouseMode.SELECTION:
            location = screen_to_grid(event_pos, self.grid_offset)
            anchored_assistant = self.assistant_at(location)
            if anchored_assistant:
                suspend_action = anchored_assistant.emitter.suspend(frame_ticks, 1000)
                if suspend_action == SuspendAction.ENTERED:
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
            t0 = session.get_synchronised_t0(frame_ticks)            
            emitter = Emitter(frame_ticks, t0, 
                              assistant.emitter_type,
                              location,
                              get_tile_rect(location, self.grid_offset).topleft,
                              assistant.speed * TILE_SIZE)
            emitter.assistant = assistant
            assistant.emitter = emitter
            # emitter will initially be suspended to synch with track timing
            # display the suspend time on screen
            countdown_text = SpriteInfoText(emitter, INFO_TEXT_OFFSET,
                                            None, "#333333", True, "#cccccc", True)
            self._sprite_infos.append(countdown_text)                                            
            timeline_logger.log(f"level: create em{emitter.id} at:{emitter.rect.center} t0:{t0}", frame_ticks)

            self._assistants.add(assistant)
            self.emitters.add(emitter)

            mouse.mode = MouseMode.SELECTION
            self.selected_assistant = None


    def handle_click_button2(self, frame_ticks, position, session, mouse):
        # if in selection mode, second mouse button removes a placed assistant
        # and moves that assistant to placement mode
        if mouse.mode == MouseMode.SELECTION:            
            location = screen_to_grid(position, self.grid_offset)
            anchored_assistant = self.assistant_at(location)
            print(f"level.handle_click_button2 - anchored_assistant:{anchored_assistant}")
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
            tile = self.tiles.get((location.x, location.y))
            if tile is not None:
                if tile.info != 'F' and tile.info != 'T':
                    track_tile_count += 1

        if track_tile_count == 1:
            return True

        return False


    def check_for_highlight(self, location):        
        highlighted_assistant = self.assistant_at(location)
        for assistant in self._assistants:
            if assistant == highlighted_assistant:
                assistant.highlight = True
            else:
                assistant.highlight = False
            assistant.redraw()

        return highlighted_assistant is not None


    def spawn_beatbug(self, due_ticks, frame_ticks):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location, self.grid_offset, due_ticks)
            timeline_logger.log(f"bug{bug.id}:spawned, t0:{bug.t0}", frame_ticks)
            self._bugs.add(bug)

            
    def on_channel_ready(self, channel_id):
        for emitter in self.emitters:
            if emitter.channel_id == channel_id:
                emitter.channel_id = None
                emitter.redraw()