import json
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from globals import *
from assistant_uibutton import AssistantUIButton
from wugga_uibutton import WuggaUIButton
from assistant import Assistant

class UI():

    def __init__(self, ui_manager, out, mouse, level):
        self.manager = ui_manager
        self._out = out
        self.mouse = mouse
        self.level = level
        self._buttons = []

        #TODO: Add exception handling for file access
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
                name = control.get("name")
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
            
                button = WuggaUIButton(rect=layout_rect,
                                       text=control["text"],
                                       manager=self.manager,
                                       anchors=element_anchors,
                                       name=name)

                self._buttons.append(button)


    def _build_assistants_palette(self):
        print("building assistants palette...")
        print("Assistant list: ", ASSISTANT_ROSTER)
        
        # build the assistants and their buttons
        for i, roster_info in enumerate(ASSISTANT_ROSTER):
            # first, the button
            x = TILE_SIZE
            y = ASSISTANT_BUTTON_SPACER * (i + 1) + i * TILE_SIZE
            colour, assistant_type = roster_info[0], roster_info[1]

            object_id = "#{}".format(colour)
            hovered_bg = self.manager.get_theme().get_colour("hovered_bg", [object_id])

            button = AssistantUIButton(rect=pygame.Rect((x, y), (TILE_SIZE * 2, TILE_SIZE)),
                                       text="",
                                       manager=self.manager,
                                       object_id=ObjectID(class_id='@assistant_buttons',
                                                          object_id=object_id),
                                       assistant_type=assistant_type,
                                       colour=colour,
                                       shadow_colour=hovered_bg)

            self._buttons.append(button)
            

    # returns topleft in screen coordinates of the tile currently
    # selected by the mouse
    def get_selected_tile(self):
        return self.mouse.sprite.rect.topleft


    def handle_gui_event(self, event, session):
        event.ui_element.on_clicked(session, self)
        

    def handle_keydown(self, key, session):
        if key == pygame.K_ESCAPE:
            session.selected_assistant = None


    def update(self, frame_ticks, time_delta, session):
        self.level.update(frame_ticks, self._out.audio)
        self.manager.update(time_delta / 1000.0)
        self.mouse.update(session, self.level)


    def draw(self, surface, session):
        self.level.draw(surface)
        self.manager.draw_ui(surface)        
        if session.selected_assistant is not None:
            session.selected_assistant_groupsingle.draw(surface)
        self.mouse.draw(surface)
        

    def pause(self):
        self.level.pause()
        

    def unpause(self, gap):
        self.level.unpause(gap)

        