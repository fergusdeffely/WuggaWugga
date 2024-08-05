import json
import copy
import pygame
import pygame_gui
from enum import Enum
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
        self._buttons = []
        self.level = Level("config/level1.json")
        self.mouse = Mouse()
        self._ui_manager = pygame_gui.UIManager(g.SCREEN_SIZE, "config/ui_theme.json")
        
        with open("config/resources.json") as f:
            d = json.load(f)
            print(d)
            self._build_controls(d["main_ui"]["controls"])

        self.rebuild_assistants_palette(self.level)


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

                self._buttons.append(button)


    def rebuild_assistants_palette(self, level):
        g.log(4, "building assistants palette...")
        g.log(4, "Assistant list: ")
        for assistant in level.assistant_roster:
            g.log(4, assistant)

        # clear any existing assistant buttons
        for button in list(self._buttons):
            if hasattr(button, "object_id"):
                if button.object_id.class_id == "@assistant_buttons":
                    self._buttons.remove(button)
        
        # build the assistants and their buttons
        for i, assistant in enumerate(level.assistant_roster):
            # first, the button
            x = g.TILE_SIZE
            y = g.ASSISTANT_BUTTON_SPACER * (i + 1) + i * g.TILE_SIZE

            button = AssistantUIButton(rect=pygame.Rect((x, y), (g.TILE_SIZE * 2, g.TILE_SIZE)),
                                       text="",
                                       manager=self._ui_manager,
                                       assistant=assistant)

            self._buttons.append(button)


    def handle_gui_event(self, cycle, event):
        if isinstance(event.ui_element, SimpleUIButton):
            self.handle_ui_button_on_clicked(event.ui_element, cycle)
        elif isinstance(event.ui_element, AssistantUIButton):
            self.handle_assistant_button_on_clicked(event.ui_element)


    def handle_ui_button_on_clicked(self, button, cycle):
        g.log(4, f"GameScreen.handle_ui_button_on_clicked {button.name}")
        if button.name == "pause_button":
            if self.level.runstate == LevelRunState.RUNNING:
                self.level.paused_at = cycle
                timeline_logger.log(f"Timeline.pause", cycle)
                self.level.pause()
                button.set_text("Unpause")
            else:               
                paused_cycles = cycle - self.level.paused_at
                timeline_logger.log(f"Timeline.unpause: paused for: {paused_cycles}", cycle)                
                self.level.unpause(paused_cycles)
                button.set_text("Pause")
        elif button.name == "test_tune_button":
            self.level.play_tune(cycle, "test_tune")


    def handle_assistant_button_on_clicked(self, button):
        if self.level.runstate == LevelRunState.RUNNING:
            g.log(4, f"UI.handle_assistant_button_on_clicked: assistant ui button {button.assistant.colour}")

            # make a copy the assistant associated with this button
            assistant = copy.deepcopy(button.assistant)
            assistant.location = self.mouse.get_grid_location(self.level.grid_offset)
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
            g.log(5, f"game_screen.process_event: MouseButtonUp : {event.button} at {g.screen_to_grid(event.pos, self.level.grid_offset)}")
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
        self.level.draw(surface)
        self._ui_manager.draw_ui(surface)
        if self.level.selected_assistant is not None:
            self.level.selected_assistant.draw(surface)
        self.mouse.draw(surface)
