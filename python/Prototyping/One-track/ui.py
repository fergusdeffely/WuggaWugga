import json
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from globals import *
from session import GameState
from assistant import Assistant

class UI():

    _elements = {}

    def __init__(self, ui_manager, surface):
        self.manager = ui_manager        
        self._surface = surface

        #TODO: Add exception handling for file access
        print("json test")
        with open("resources.json") as f:
            d = json.load(f)
            print(d)
            self._build_controls(d["main_ui"]["controls"])

        self._build_assistants_palette()


    def _build_controls(self, controls):
        print("building controls...")

        for control in controls:
            element_anchors = {}
            layout_rect = None
            if control["type"] == "button":
                rect = control.get("rect")
                if rect is not None:
                    layout_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
                    print("layout rect:{}".format(layout_rect))
                anchors = control.get("anchors")
                if anchors is not None:
                    print("anchors:{}".format(anchors))
                    for to, offset in anchors.items():
                        if to == "right":
                            layout_rect.right = 0 - offset
                            element_anchors["right"] = "right"
                        if to == "bottom":
                            layout_rect.bottom = 0 - offset
                            element_anchors["bottom"] = "bottom"
                    print("element_anchors: {}".format(element_anchors))
            
                button = pygame_gui.elements.UIButton(relative_rect=layout_rect,
                                                      text=control["text"],
                                                      manager=self.manager,
                                                      anchors=element_anchors)
                self._elements[button] = self.on_pause_clicked


    def _build_assistants_palette(self):
        print("building assistants palette...")
        print("Assistant list: ", ASSISTANT_LIST)

        # build the assistants
        for i, a in enumerate(ASSISTANT_LIST):
            x = TILE_SIZE
            y = ASSISTANT_BUTTON_SPACER * (i + 1) + i * TILE_SIZE
            object_id = "#{}".format(a[0])
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), (TILE_SIZE * 2, TILE_SIZE)),
                                                    text="",
                                                    manager=self.manager,
                                                    object_id=ObjectID(class_id='@assistant_buttons',
                                                                       object_id=object_id))
            assistant = Assistant(a[0], a[1])
            self._elements[button] = assistant.on_clicked


    def handle_gui_event(self, event, session):
        handler = self._elements.get(event.ui_element)
        handler(event.ui_element, session)


    def on_pause_clicked(self, ui_element, session):
        print("on_pause_clicked")
        if session.gamestate == GameState.RUNNING:
            session.timeline.pause()
            session.gamestate = GameState.PAUSED
            ui_element.text = "Unpause"
        else:
            session.timeline.unpause()
            session.gamestate = GameState.RUNNING
            ui_element.text = "Pause"


    def draw(self, surface):
        self.manager.draw_ui(surface)


    def update(self, time_delta):
        self.manager.update(time_delta)
        