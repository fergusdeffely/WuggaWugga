import pygame
import copy
import json
from enum import Enum

import globals as g
from timeline_logger import timeline_logger
from timeline import Timeline
from timeline_event import TimelineEvent
from assistant import Assistant
from spark import Spark
from path import Path
from emitter import Emitter
from mouse import MouseMode
from info_text import InfoText
from info_text import SpriteInfoText
from tune import Tune
from ui.assistant_uibutton import AssistantUIButton


class LevelRunState(Enum):
    INITIALISING = 0
    RUNNING = 1
    PAUSED = 2
    PLAY_TUNE = 3


class Level():

    def __init__(self, level_filename, frame):
        self.runstate = LevelRunState.INITIALISING
        self._assistants = pygame.sprite.Group()
        self._paths = []
        self.emitters = pygame.sprite.Group()
        self._sprite_infos = []
        self.assistant_roster = []
        self.selected_assistant = None
        self._timeline = Timeline()
        
        with open(level_filename) as f:
            d = json.load(f)
            self._parse_config(d, frame)
        

    def screen_to_view(self, pos):
        return (pos[0] - self.view.left, pos[1] - self.view.top)


    def _parse_config(self, json, inner_frame):

        g.log(4, f"level data:\n{json}")
        self.width_in_tiles = json["width"]
        self.height_in_tiles = json["height"]
        self.width = self.width_in_tiles * g.GRID_SIZE
        self.height = self.height_in_tiles * g.GRID_SIZE

        # the area where this level will be drawn
        x = inner_frame.left + (inner_frame.width - self.width) / 2
        y = inner_frame.top + (inner_frame.height - self.height) / 2
        
        self.view = pygame.Rect(x, y, self.width , self.height)

        g.log(3, f"level: view: {self.view}")

        # create the assistant roster
        for name, data in json["assistants"].items():
            self.assistant_roster.append(Assistant(name, data))

        # add the paths
        for name, data in json["paths"].items():
            self._paths.append(Path(name, data, self._timeline))

        self.runstate = LevelRunState.RUNNING


    def play_tune(self, cycle, name):
        self.pause(cycle)
        self.runstate = LevelRunState.PLAY_TUNE
        track = {32:"onekick", 64:"onekick", 96:"synthbass", 128:"onekick"}
        self.tune = Tune([track])
        self.tune.play(cycle)


    def update(self, cycle, audio):
        self._timeline.update(cycle)
        
        if self.runstate == LevelRunState.RUNNING:
            # update emitters first
            self.emitters.update(cycle)
            # note: path updates move sparks and check for collisions
            for path in self._paths:
                path.update(cycle, self, audio)
            for sprite_info in list(self._sprite_infos):
                if sprite_info.update(cycle) == False:
                    self._sprite_infos.remove(sprite_info)
        elif self.runstate == LevelRunState.PLAY_TUNE:
            self.tune.play_at(cycle, audio)
                

    def draw(self, surface):

        # create a surface for the view
        view_surface = pygame.Surface(self.view.size)

        # border
        pygame.draw.rect(view_surface, "white", pygame.Rect(0, 0, self.view.width, self.view.height), 2)

        if g.DRAW_GRID == True:
            self.draw_grid(view_surface)
        for path in self._paths:
            path.draw(view_surface)
        self._assistants.draw(view_surface)
        self.emitters.draw(view_surface)
        for path in self._paths:
            path.draw_sparks(view_surface)
        for sprite_info_text in self._sprite_infos:
            sprite_info_text.draw(view_surface)  
        
        surface.blit(view_surface, self.view.topleft)


    def pause(self, runstate):
        self.runstate = runstate
        self._timeline.pause()        


    def unpause(self, paused_cycles):
        self.runstate = LevelRunState.RUNNING

        for emitter in self.emitters:
            emitter.adjust_for_pause(paused_cycles)

        self._timeline.unpause(paused_cycles)        


    def draw_grid(self, surface):
        # vertical lines
        for x in range(self.width_in_tiles + 1):
            pygame.draw.line(surface, "#35353575", 
                             (x * g.GRID_SIZE, 2),
                             (x * g.GRID_SIZE, self.height - 4))

        # horiztonal lines
        for y in range(self.height_in_tiles + 1):
            pygame.draw.line(surface, "#35353575", 
                             (2, y * g.GRID_SIZE),
                             (self.width - 4, y * g.GRID_SIZE))


    def handle_click_button1(self, cycle, screen_pos, mouse):
        view_pos = self.screen_to_view(screen_pos)

        if mouse.mode == MouseMode.SELECTION:
            location = g.pos_to_loc(view_pos)
            anchored_assistant = self.assistant_at(location)
            # clicked an assistant?
            if anchored_assistant:
                # suspend the emitter
                # but... don't suspend emitters that are currently playing sounds
                if anchored_assistant.emitter.play_counter <= 0:
                    suspend_action = anchored_assistant.emitter.suspend(cycle, g.SUSPEND_FRAMES)
                    if suspend_action == g.SuspendAction.SUSPENDED:
                        countdown_text = SpriteInfoText(anchored_assistant.emitter, 
                                                        g.INFO_TEXT_OFFSET,
                                                        None, "#333333", True, "#cccccc", True)
                        self._sprite_infos.append(countdown_text)
            return

        if self.selected_assistant == None:
            return

        if self.is_assistant_placeable(self.selected_assistant):
            # add a new assistant to the level
            location = g.pos_to_loc(view_pos)
            # set the assistant into the level
            assistant = copy.deepcopy(self.selected_assistant)
            assistant.anchored = True
            # create an emitter

            synch_cycle = g.get_synchronised_cycle(cycle, assistant.speed)

            emitter = Emitter(synch_cycle,
                              assistant.emit_sound,
                              assistant.play_duration,
                              location,
                              g.get_tile_rect(location).topleft,
                              assistant.speed)
            emitter.assistant = assistant
            assistant.emitter = emitter
            # emitter will initially be suspended for better timing synch 
            # display the suspend time on screen
            countdown_text = SpriteInfoText(emitter, g.INFO_TEXT_OFFSET,
                                            None, "#333333", True, "#cccccc", True)
            self._sprite_infos.append(countdown_text)                                            
            timeline_logger.log(f"em{emitter.id} create at: {emitter.rect.center} synch at: {synch_cycle}", cycle)

            self._assistants.add(assistant)
            self.emitters.add(emitter)

            mouse.mode = MouseMode.SELECTION
            self.selected_assistant = None


    def handle_click_button2(self, cycle, screen_pos, mouse):
        view_pos = self.screen_to_view(screen_pos)
        # if in selection mode, second mouse button removes a placed assistant
        # and moves that assistant to placement mode
        if mouse.mode == MouseMode.SELECTION:
            location = g.vie_to_grid(view_pos)
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
                self.selected_assistant.rotate()
                if self.is_assistant_placeable(self.selected_assistant):
                    self.selected_assistant.redraw()
                else:
                    self.selected_assistant.redraw(self.selected_assistant.shadow_colour)                
                

    def assistant_at(self, location):
        for assistant in self._assistants.sprites():
            if assistant.has_node(location):
                return assistant

        return None


    def is_assistant_placeable(self, assistant):
        locations = assistant.get_node_locations()
        path_tile_count = 0
        for location in locations:
            if g.x(location) < 0 or g.y(location) < 0:
                continue
            if g.x(location) >= self.width_in_tiles or g.y(location) >= self.height_in_tiles:
                continue
            # can't place over another assistant
            if self.assistant_at(location) is not None:
                return False
            
            for path in self._paths:
                tile = path.tiles.get((location.x, location.y))
                if tile is not None:
                    if tile.info != 'F' and tile.info != 'T':
                        path_tile_count += 1

        if path_tile_count == 1:
            return True

        return False


    def on_new_mouse_location(self, screen_pos):
        # return is True if the mouse outline should be hidden
        pos = self.screen_to_view(screen_pos)
        location = g.pos_to_loc(pos)

        assistant_at_location = self.assistant_at(location)
        
        for assistant in self._assistants:
            if assistant == assistant_at_location:
                assistant.highlight = True
            else:
                assistant.highlight = False
            assistant.redraw()

        if(location.x < 0 or location.x >= self.width_in_tiles or
           location.y < 0 or location.y >= self.height_in_tiles):
           return True

        return assistant_at_location is not None
