import json
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from globals import *
from assistant_uibutton import AssistantUIButton
from wugga_uibutton import WuggaUIButton
from assistant import Assistant
from mouse import MouseMode

class UI():

    def __init__(self, ui_manager, out, mouse, level):
        self._out = out
        self._buttons = []
        self.manager = ui_manager        
        self.mouse = mouse
        self.level = level

        with open("config/resources.json") as f:
            d = json.load(f)
            print(d)
            self._build_controls(d["main_ui"]["controls"])

        self.rebuild_assistants_palette(self.level)


    def _build_controls(self, controls):
        log(4, "_build_controls:")

        for control in controls:
            element_anchors = {}
            layout_rect = None
            if control["type"] == "button":
                rect = control.get("rect")
                if rect is not None:
                    layout_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
                    log(4, "layout rect:{}".format(layout_rect))
                name = control.get("name")
                anchors = control.get("anchors")
                if anchors is not None:
                    log(4, "anchors:{}".format(anchors))
                    for to, offset in anchors.items():
                        if to == "right":
                            layout_rect.right = 0 - offset
                            element_anchors["right"] = "right"
                        if to == "bottom":
                            layout_rect.bottom = 0 - offset
                            element_anchors["bottom"] = "bottom"
                    log(4, "element_anchors: {}".format(element_anchors))
            
                button = WuggaUIButton(rect=layout_rect,
                                       text=control["text"],
                                       manager=self.manager,
                                       anchors=element_anchors,
                                       name=name)

                self._buttons.append(button)


    def rebuild_assistants_palette(self, level):
        log(4, "building assistants palette...")
        log(4, "Assistant list: ")
        for assistant in level.assistant_roster:
            log(4, assistant)

        # clear any existing assistant buttons
        for button in list(self._buttons):
            if hasattr(button, "object_id"):
                if button.object_id.class_id == "@assistant_buttons":
                    self._buttons.remove(button)
        
        # build the assistants and their buttons
        for i, assistant in enumerate(level.assistant_roster):
            # first, the button
            x = TILE_SIZE
            y = ASSISTANT_BUTTON_SPACER * (i + 1) + i * TILE_SIZE

            button = AssistantUIButton(rect=pygame.Rect((x, y), (TILE_SIZE * 2, TILE_SIZE)),
                                       text="",
                                       manager=self.manager,
                                       assistant=assistant)

            self._buttons.append(button)
            

    def get_mouse_location(self):
        return screen_to_grid(self.mouse.rect.topleft, self.level.grid_offset)


    def handle_gui_event(self, cycle, event, timeline):
        event.ui_element.on_clicked(cycle, self, timeline)
        

    def handle_keydown(self, key, mouse):
        if key == pygame.K_ESCAPE:
            self.level.selected_assistant = None            
            mouse.mode = MouseMode.SELECTION


    def update(self, cycle, time_delta):
        self.level.update(cycle, self._out.audio)
        self.manager.update(time_delta / 1000.0)
        self.mouse.update(self.level)


    def draw(self, surface):
        self.level.draw(surface)
        self.manager.draw_ui(surface)
        if self.level.selected_assistant is not None:
            self.level.selected_assistant.draw(surface)
        self.mouse.draw(surface)
        

    def pause(self):        
        self.level.pause()
                