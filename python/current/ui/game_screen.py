import json
import copy
import pygame
from enum import Enum
import pygame_gui
from pygame_gui.elements import UIPanel

import globals as g
from mouse import Mouse
from mouse import MouseMode
from timeline import Timeline
from timeline_logger import timeline_logger
from level import Level
from level import LevelRunState
from ui.simple_uibutton import SimpleUIButton
from ui.assistant_uibutton import AssistantUIButton


class GameScreen():

    def __init__(self):
        self.cycle = 0
        self._buttons = {}

        # the area inside the margins where levels can be drawn
        self._inner_frame = pygame.Rect(g.LEVEL_MARGIN_LEFT * g.GRID_SIZE,
                                        g.LEVEL_MARGIN_TOP * g.GRID_SIZE,
                                        g.INNER_FRAME_WIDTH * g.GRID_SIZE,
                                        g.INNER_FRAME_HEIGHT * g.GRID_SIZE)

        g.log(3, f"gamescreen: inner_frame: {self._inner_frame}")

        self.level = Level("config/level1.json", self._inner_frame)
        self.mouse = Mouse()
        self._ui_manager = pygame_gui.UIManager(g.SCREEN_SIZE, "config/ui_theme.json")
        
        with open("config/resources.json") as f:
            d = json.load(f)
            print(d)
            self._build_controls(d["main_ui"]["controls"])

        panel_height = len(self.level.assistant_roster) * (g.ASSISTANT_BUTTON_SPACER + g.GRID_SIZE) + g.ASSISTANT_BUTTON_SPACER
        panel_width = g.ASSISTANT_BUTTON_WIDTH + g.ASSISTANT_BUTTON_SPACER * 2

        self._assistants_panel = UIPanel(pygame.Rect(g.GRID_SIZE, g.GRID_SIZE * 2, panel_width, panel_height),
                                         starting_height=4,
                                         manager=self._ui_manager)

        # add buttons for the current level's assistants
        self._build_assistant_buttons()


    def _build_controls(self, controls):
        g.log(4, "_build_controls:")

        for control in controls:
            element_anchors = {}
            layout_rect = None
            if control["type"] == "button":
                rect = control.get("rect")
                if rect is not None:
                    layout_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
                    g.log(4, "layout rect:{}".format(layout_rect))
                name = control.get("name")
                anchors = control.get("anchors")
                if anchors is not None:
                    g.log(4, "anchors:{}".format(anchors))
                    for to, offset in anchors.items():
                        if to == "right":
                            layout_rect.right = 0 - offset
                            element_anchors["right"] = "right"
                        if to == "bottom":
                            layout_rect.bottom = 0 - offset
                            element_anchors["bottom"] = "bottom"
                    g.log(4, "element_anchors: {}".format(element_anchors))
            
                button = SimpleUIButton(rect=layout_rect,
                                       text=control["text"],
                                       manager=self._ui_manager,
                                       anchors=element_anchors,
                                       name=name)

                self._buttons[name] = button


    def _build_assistant_buttons(self):

        g.log(4, "game_screen: building assistants palette...")
        g.log(4, "game_screen: Assistant list: ")
        
        for assistant in self.level.assistant_roster:
            g.log(4, f"           {assistant}")

        buttons = []
        for i, assistant in enumerate(self.level.assistant_roster):
            # first, the button
            x = g.ASSISTANT_BUTTON_SPACER
            y = g.ASSISTANT_BUTTON_SPACER * (i + 1) + i * g.ASSISTANT_BUTTON_HEIGHT

            button = AssistantUIButton(rect=pygame.Rect((x, y), (g.ASSISTANT_BUTTON_WIDTH, g.ASSISTANT_BUTTON_HEIGHT)),
                                       text="",
                                       manager=self._ui_manager,
                                       assistant=assistant,
                                       container=self._assistants_panel)

            self._buttons[button.name] = button


    def handle_gui_event(self, cycle, event):
        if isinstance(event.ui_element, SimpleUIButton):
            self.handle_ui_button_on_clicked(cycle, event.ui_element)
        elif isinstance(event.ui_element, AssistantUIButton):
            self.handle_assistant_button_on_clicked(event.ui_element)


    def handle_ui_button_on_clicked(self, cycle, button):
        g.log(4, f"GameScreen.handle_ui_button_on_clicked {button.name}")
        if button.name == "pause_button":
            self._handle_pause_button_pressed(cycle)
        elif button.name == "test_tune_button":
            # first simulate pause button being pressed
            self._handle_pause_button_pressed(cycle)
            # now play the tune
            self.level.play_tune(cycle, "test_tune")


    def _handle_pause_button_pressed(self, cycle):
        button = self._buttons["pause_button"]
        if self.level.runstate == LevelRunState.RUNNING:
            self.paused_at = cycle
            timeline_logger.log(f"GameScreen.pause", cycle)
            self.level.pause(LevelRunState.PAUSED)
            button.set_text("Unpause")
        else:
            paused_cycles = cycle - self.paused_at
            timeline_logger.log(f"GameScreen.unpause: paused for: {paused_cycles}", cycle)
            self.level.unpause(paused_cycles)
            button.set_text("Pause")


    def handle_assistant_button_on_clicked(self, button):
        if self.level.runstate == LevelRunState.RUNNING:
            g.log(4, f"UI.handle_assistant_button_on_clicked: assistant ui button {button.assistant.colour}")

            # make a copy the assistant associated with this button
            assistant = copy.deepcopy(button.assistant)
            assistant.location = self.mouse.get_grid_location()
            g.log(4, f"Created assistant: {assistant}")

            self.level.selected_assistant = assistant

            # refresh the mouse
            self.mouse.mode = MouseMode.PLACEMENT
            self.mouse.draw_cursor()


    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.level.selected_assistant = None
            self.mouse.mode = MouseMode.SELECTION


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            g.log(5, f"game_screen.process_event: MouseButtonUp : {event.button} at {event.pos}")
            # was the mouse clicked within the bounds of the level?
            if self.level.view.collidepoint(event.pos):
                if event.button == 1:
                    if self.level.runstate == LevelRunState.RUNNING:
                        self.level.handle_click_button1(self.cycle, event.pos, self.mouse)
                if event.button == 3:
                    if self.level.runstate == LevelRunState.RUNNING:
                        self.level.handle_click_button2(self.cycle, event.pos, self.mouse)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.handle_keydown(event.key)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            g.log(5, f"Event{event.type}: pygame_gui.UI_BUTTON_PRESSED : {event}")            
            self.handle_gui_event(self.cycle, event)

        self._ui_manager.process_events(event)


    def update(self, time_delta, audio):
        self.level.update(self.cycle, audio)
        self._ui_manager.update(time_delta / 1000.0)
        self.mouse.update(self.level)
        self.cycle += 1


    def draw(self, surface):
        surface.fill("black")
        pygame.draw.rect(surface, "#75757575", self._inner_frame, width=1)        
        self.level.draw(surface)
        self._ui_manager.draw_ui(surface)
        if self.level.selected_assistant is not None:
            self.level.selected_assistant.draw(surface)
        self.mouse.draw(surface)
