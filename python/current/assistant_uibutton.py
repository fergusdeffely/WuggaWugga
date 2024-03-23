from enum import Enum
import copy
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from globals import *
from level import LevelRunState
from assistant import Assistant
from mouse import MouseMode


class AssistantUIButton(pygame_gui.elements.UIButton):

    def __init__(self, rect, text, manager, assistant):
        object_id = ObjectID(class_id='@assistant_buttons', 
                             object_id=get_html_colour(assistant.colour))
        super().__init__(relative_rect=rect, text=text, manager=manager, object_id=object_id)

        self.assistant = assistant


    def on_clicked(self, ui, session):
        if ui.level.runstate == LevelRunState.RUNNING:
            log(4, f"on_clicked: assistant ui button {self.assistant.colour}")

            # make a copy the assistant associated with this button
            assistant = copy.deepcopy(self.assistant)
            assistant.location = ui.get_mouse_location()
            log(4, f"Created assistant: {assistant}")

            ui.level.selected_assistant = assistant

            # refresh the mouse
            ui.mouse.mode = MouseMode.PLACEMENT
            ui.mouse.draw_cursor()





    

