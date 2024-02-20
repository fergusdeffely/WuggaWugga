import pygame
import pygame_gui
from globals import *
from session import GameState
from assistant import Assistant

class UI():

    _elements = {}

    def __init__(self, ui_manager, session):
        self.manager = ui_manager

        self._build_controls()
        self._build_assistants_palette()


    def _build_controls(self):
        print("building controls...")
        pos = grid_to_screen((4, 1))
        pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, (100, 50)),
                                                    text='Pause',
                                                    manager=self.manager)
        self._elements[pause_button] = self.on_pause_clicked


    def _build_assistants_palette(self):
        print("building assistants palette...")
        print("Assistant list: ", ASSISTANT_LIST)

        # build the assistants
        for i, colour in enumerate(ASSISTANT_LIST):
            location = (1, 1 + i*2)
            pos = grid_to_screen(location)
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(pos, (TILE_SIZE * 2, TILE_SIZE)),
                                                    text=colour,
                                                    manager=self.manager)
            
            assistant = Assistant(colour)
            self._elements[button] = assistant.on_clicked
            

    def handle_gui_event(self, event, session):
        for element in self._elements:
            if event.ui_element == element:
                # elements dict stores handler methods as values
                self._elements[element](session)


    def on_pause_clicked(self, session):
        print("on_pause_clicked")
        if session.gamestate == GameState.RUNNING:
            session.timeline.pause()
            session.gamestate = GameState.PAUSED
        else:
            session.timeline.unpause()
            session.gamestate = GameState.RUNNING


    def draw(self, surface):
        self.manager.draw_ui(surface)


    def update(self, time_delta):
        self.manager.update(time_delta)
        