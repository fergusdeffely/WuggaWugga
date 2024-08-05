from enum import Enum
import pygame
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

from globals import *
from level import LevelRunState
from assistant import Assistant
from mouse import MouseMode


class AssistantUIButton(UIButton):

    def __init__(self, rect, text, manager, assistant):
        object_id = ObjectID(class_id='@assistant_buttons', 
                             object_id=get_html_colour(assistant.colour))
        super().__init__(relative_rect=rect, text=text, manager=manager, object_id=object_id)

        self.assistant = assistant
