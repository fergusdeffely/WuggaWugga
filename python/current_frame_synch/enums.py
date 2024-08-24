from enum import Enum

class MenuOption(Enum):
    MAIN_CONTINUE = 0
    MAIN_NEW_GAME = 1
    MAIN_OPTIONS = 2
    MAIN_EXIT = 3

class TransitionType(Enum):
    BARN_DOOR_TRANSITION = 0
    RISING_FLOOD_TRANSITION = 1

