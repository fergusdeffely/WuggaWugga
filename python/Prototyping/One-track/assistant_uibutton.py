from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState
from assistant import Assistant

class AssistantUIButton(pygame_gui.elements.UIButton):

    def __init__(self, rect, text, manager, object_id, assistant_type, colour, shadow_colour):
        super().__init__(relative_rect=rect, text=text, manager=manager, object_id=object_id)

        self.type = assistant_type
        self.colour = colour
        # lower the alpha for the shadow colour
        shadow_colour[3] = 150
        self.shadow_colour = shadow_colour


    def on_clicked(self, session, ui):
        if session.gamestate == GameState.RUNNING:
            print(f"on_clicked: assistant {self.colour}")

            # create an assistant
            assistant = Assistant(self.type, self.colour, self.shadow_colour)
            session.selected_assistant = assistant

            # refresh the mouse
            location = screen_to_grid(pygame.mouse.get_pos())
            ui.mouse.sprite.redraw_mouse_pointer(session, ui.level, location)



    

