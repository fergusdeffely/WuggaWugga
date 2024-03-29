import pygame
import copy
from globals import *
from timeline_logger import timeline_logger
from tracktile import TrackTile
from beatbug import BeatBug
from emitter import Emitter
from mouse import MouseMode
from info_text import InfoText
from info_text import SpriteInfoText

class Level:

    def __init__(self, data, out):
        self._out = out
        self._data = data
        self._tiles = pygame.sprite.Group()
        self._assistants = pygame.sprite.Group()
        self._bugs = pygame.sprite.Group()
        self._emitters = pygame.sprite.Group()
        self._sprite_infos = []
        self._initialise(data)
        self._paused = False


    def _initialise(self, data):
        # add the tiles        
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell in ['N', 'S', 'W', 'E']:
                    tile = TrackTile((x, y), cell)
                    self._tiles.add(tile)
                elif cell == 'B':
                    # Begin
                    self._spawner_location = (x, y)
                elif cell == 'F':
                    # Finish
                    self.finish_location = (x, y)


    def update(self, frame_ticks, audio):
        if self._paused == False:
            self._tiles.update()
            # emitters need to know where bugs are and bugs need
            # to know where emitters are            
            self._emitters.update(frame_ticks, self._bugs, audio)
            self._bugs.update(frame_ticks, self._data, self._emitters, audio)
            for sprite_info in list(self._sprite_infos):
                if sprite_info.update(frame_ticks) == False:
                    self._sprite_infos.remove(sprite_info)
                


    def draw(self, surface):
        if DRAW_GRID == True:
            self.draw_grid(surface)
        self._tiles.draw(surface)
        self._assistants.draw(surface)
        self._emitters.draw(surface)
        self._bugs.draw(surface)
        for sprite_info_text in self._sprite_infos:
            sprite_info_text.draw(surface)


    def pause(self):
        self._paused = True


    def unpause(self, gap):
        self._paused = False
        for bug in self._bugs:
            bug.adjust_for_pause(gap)

        for emitter in self._emitters:
            emitter.adjust_for_pause(gap)


    def draw_grid(self, surface):
        width_in_tiles = len(self._data[0])
        height_in_tiles = len(self._data)

        # vertical lines
        for x in range(width_in_tiles):
            pygame.draw.line(surface, "#75757575", (x*TILE_SIZE, 0), (x*TILE_SIZE, height_in_tiles * TILE_SIZE))

        # horiztonal lines
        for y in range(height_in_tiles):
            pygame.draw.line(surface, "#75757575", (0, y*TILE_SIZE), (width_in_tiles * TILE_SIZE, y*TILE_SIZE))


    def handle_click_button1(self, frame_ticks, position, session, mouse):
        if mouse.mode == MouseMode.SELECTION:
            location = screen_to_grid(position)
            anchored_assistant = self.assistant_at(location)
            if anchored_assistant:
                suspend_action = anchored_assistant.emitter.suspend(frame_ticks, 1000)
                if suspend_action == SuspendAction.ENTERED:
                    countdown_text = SpriteInfoText(anchored_assistant.emitter, 
                                                    INFO_TEXT_OFFSET,
                                                    None, "#333333", True, "#cccccc", True)
                    self._sprite_infos.append(countdown_text)
            return

        if session.selected_assistant == None:
            return

        if self.is_assistant_placeable(session.selected_assistant):
            location = screen_to_grid(position)
            # set the assistant into the level
            assistant = copy.deepcopy(session.selected_assistant)
            assistant.anchored_location = location
            # create an emitter
            t0 = session.get_synchronised_t0(frame_ticks)
            emitter = Emitter(frame_ticks, t0, assistant.emitter_type, location, assistant.colour)
            emitter.assistant = assistant
            assistant.emitter = emitter
            # emitter will initially be suspended to synch with track timing
            # display the suspend time
            countdown_text = SpriteInfoText(emitter, INFO_TEXT_OFFSET,
                                            None, "#333333", True, "#cccccc", True)
            self._sprite_infos.append(countdown_text)                                            
            timeline_logger.log(f"level: create em{emitter.id} at:{emitter.rect.center} t0:{t0}", frame_ticks)

            # add a new assistant to the level
            self._assistants.add(assistant)
            self._emitters.add(emitter)
            mouse.mode = MouseMode.SELECTION

            session.selected_assistant_groupsingle = None


    def handle_click_button2(self, frame_ticks, position, session, mouse):
        # if in selection mode, second mouse button removes a placed assistant
        # and moves that assistant to placement mode
        if mouse.mode == MouseMode.SELECTION:
            location = screen_to_grid(position)
            anchored_assistant = self.assistant_at(location)
            if anchored_assistant:
                # detach the assistant
                # first, remove any associated info text            
                for sprite_info in list(self._sprite_infos):
                    if sprite_info.has_sprite(anchored_assistant.emitter):
                        self._sprite_infos.remove(sprite_info)
                self._emitters.remove(anchored_assistant.emitter)
                self._assistants.remove(anchored_assistant)
                session.selected_assistant = anchored_assistant
                session.selected_assistant.anchored_location = None

                mouse.mode = MouseMode.PLACEMENT

            return

        if mouse.mode == MouseMode.PLACEMENT:
            if session.selected_assistant is not None:
                session.selected_assistant.rotate()
                if self.is_assistant_placeable(session.selected_assistant) == False:
                    session.selected_assistant.redraw(session.selected_assistant.shadow_colour)
                else:
                    session.selected_assistant.redraw()
                


    def assistant_at(self, location):
        for assistant in self._assistants.sprites():
            if assistant.has_node(location):
                return assistant

        return None


    def track_tile_at(self, location):
        # check if the location is valid for placement
        cell = self._data[y(location)][x(location)]

        if(cell in "NSEW"):        
            return True
        else:
            return False


    def is_assistant_placeable(self, assistant):
        locations = assistant.get_node_locations()
        track_tile_count = 0
        for location in locations:
            if x(location) < 0 or y(location) < 0:
                continue
            if x(location) >= SCREEN_WIDTH_TILES or y(location) >= SCREEN_HEIGHT_TILES:
                continue
            if self.assistant_at(location) is not None:
                return False
            if self.track_tile_at(location):
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
            bug = BeatBug(self._spawner_location, due_ticks)
            timeline_logger.log(f"bug{bug.id}:spawned, t0:{bug.t0}", frame_ticks)
            self._bugs.add(bug)

            
    def on_channel_ready(self, channel_id):
        for emitter in self._emitters:
            if emitter.channel_id == channel_id:
                emitter.channel_id = None
                emitter.redraw()