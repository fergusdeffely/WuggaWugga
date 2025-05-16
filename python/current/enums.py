from enum import Enum

class MenuOption(Enum):
    MAIN_CONTINUE = 0
    MAIN_NEW_GAME = 1
    MAIN_OPTIONS = 2
    MAIN_EXIT = 3

class TransitionType(Enum):
    TRANSITION_NONE         = 0
    BARN_DOOR_TRANSITION    = 1
    RISING_FLOOD_TRANSITION = 2

