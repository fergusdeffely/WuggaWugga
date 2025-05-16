import numpy
import pygame
import pygame_gui
from enums import *

LOGGING_LEVEL = 3
LOG_FRAME_DELTAS = False
LOG_SPARK_MOVEMENT = True

FRAMES_PER_SECOND = 64
SUSPEND_FRAMES = int(FRAMES_PER_SECOND / 2)

NULL_LOCATION = (None, None)
GRID_SIZE = 32

#  ----------------------------------------------------------
# |                                                          |  < LEVEL_MARGIN_TOP
# |      --------------------------------------------------  | 
# |     |      INNER_FRAME_WIDTH                           | |
# |     |              X                                   | |
# |     |      INNER_FRAME_HEIGHT                          | |
# |     |                                                  | |
# |     |        ----------------------------------        | |
# |     |       |                                  |       | |
# |     |       |                                  |       | |
# |     |       |                                  |       | |
# |     |       |      Level.view                  |       | |
# |     |       |                                  |       | |
# |     |       |                                  |       | |
# |     |       |                                  |       | |
# |     |       |                                  |       | |
# |     |        ----------------------------------        | |
# |     |                                                  | |
# |     |                                                  | |
# |     |                                                  | |
# |      --------------------------------------------------  | 
#  ----------------------------------------------------------
#     ^
#  LEVEL_MARGIN_LEFT

# level view margins are defined in terms of tiles
LEVEL_MARGIN_LEFT = 3
LEVEL_MARGIN_TOP = 1
LEVEL_MARGIN_RIGHT = 1
LEVEL_MARGIN_BOTTOM = 1
INNER_FRAME_WIDTH = 28
INNER_FRAME_HEIGHT = 14

SCREEN_WIDTH_TILES = INNER_FRAME_WIDTH + LEVEL_MARGIN_LEFT + LEVEL_MARGIN_RIGHT
SCREEN_HEIGHT_TILES = INNER_FRAME_HEIGHT + LEVEL_MARGIN_TOP + LEVEL_MARGIN_BOTTOM
SCREEN_WIDTH_PIXELS = SCREEN_WIDTH_TILES * GRID_SIZE
SCREEN_HEIGHT_PIXELS = SCREEN_HEIGHT_TILES * GRID_SIZE
SCREEN_SIZE = (SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS)

DRAW_GRID = True

DEFAULT_SPARK_SPEED = 2                         # number of pixels moved in a frame
SPARK_SIZE = pygame.Vector2(15, 15)
SPARK_HITBOX_SIZE = pygame.Vector2(10, 10)
SPARK_ANIM_STEP = 10

PATHNODE_SIZE = pygame.Vector2(8, 8)

BEATBUG_SIZE = 32
BEATBUG_HITBOX_SIZE = 10
BEATBUG_ANIM_STEP = 10


H_CENTER_BEATBUG = (GRID_SIZE - BEATBUG_SIZE) / 2
V_CENTER_BEATBUG = (GRID_SIZE - BEATBUG_SIZE) / 2

EMITTER_SPEED = GRID_SIZE
EMITTER_RADIUS = GRID_SIZE / 3
EMITTER_HITBOX_SIZE = 10

VECTOR_NORTH = pygame.Vector2(0,-1)
VECTOR_SOUTH = pygame.Vector2(0, 1)
VECTOR_EAST  = pygame.Vector2(1, 0)
VECTOR_WEST  = pygame.Vector2(-1,0)

FONT_SIZE = 16
INFO_TEXT_OFFSET = pygame.Vector2(0, 0 - GRID_SIZE * 3 / 4)

MENU_BUTTON_WIDTH = 300
MENU_BUTTON_HEIGHT = 30
MENU_BUTTON_SEPARATOR = 5

BASE_WUGGA_USEREVENT = pygame_gui.UI_TEXT_EFFECT_FINISHED + 1
#CHANNEL_READY_EVENT = BASE_WUGGA_USEREVENT + 0

ASSISTANT_BUTTON_SPACER = GRID_SIZE / 2
ASSISTANT_BUTTON_WIDTH = GRID_SIZE * 2
ASSISTANT_BUTTON_HEIGHT = GRID_SIZE

DEBUG_SHOW_HITBOXES = False

# Transitions
MAX_FLOOD_LEVEL = 50
FLOOD_FADE_1 = 60
FLOOD_FADE_2 = 35
FLOOD_FADE_3 = 15


class SuspendAction(Enum):
    SUSPENDED = 0
    EXTENDED = 1

def x(coords):
    return coords[0]

def y(coords):
    return coords[1]
        
def N(exit):
    return exit[0]

def S(exit):
    return exit[1]

def E(exit):
    return exit[2]

def W(exit):
    return exit[3]

def parse_location_text(location_text):
    i = location_text.find(':')
    return (int(location_text[:i]), int(location_text[i+1:]))

def loc_to_pos(location):
    # returns topleft of a location's grid
    return ((location[0]) * GRID_SIZE, 
            (location[1]) * GRID_SIZE)

def pos_to_loc(position):
    return pygame.Vector2(int(position[0] / GRID_SIZE),
                          int(position[1] / GRID_SIZE))

def get_tile_topleft(position):
    left = position[0] - position[0] % GRID_SIZE
    top = position[1] - position[1] % GRID_SIZE
    return (left, top)

def get_tile_rect(location):
    topleft = grid_to_view(location)
    return pygame.Rect(x(topleft), y(topleft), GRID_SIZE, GRID_SIZE)
  
def get_direction_vector(bearing):
    if bearing == 'N':
        return pygame.math.Vector2(0,-1)
    elif bearing == 'S':
        return pygame.math.Vector2(0,1)
    elif bearing == 'W':
        return pygame.math.Vector2(-1,0)
    elif bearing == 'E' or bearing == 'B':  
        return pygame.math.Vector2(1,0)
      
    return pygame.math.Vector2(0,0)


def get_normalised_direction_vector(from_pos, to_pos):
    return (to_pos - from_pos).normalize()
  

def add_tuples(tup1, tup2):
    return tuple(map(lambda i, j: i + j, tup1, tup2))


def get_synchronised_cycle(cycle, speed):
    rem = cycle % FRAMES_PER_SECOND    

    if rem == 0:
        # this cycle is a synch frame
        return cycle
    else:
        # wait for next synch frame
        return cycle - rem + FRAMES_PER_SECOND

def log(level, message):
    if level <= LOGGING_LEVEL:
        print(message)

def get_html_colour(colour):
    return f"#{colour.r:02x}{colour.g:02x}{colour.b:02x}"


def greyscale(surface):
    arr = pygame.surfarray.pixels3d(surface)    
    mean_arr = numpy.dot(arr[:, :, :], [0.216, 0.587, 0.144])    
    mean_arr3d = mean_arr[..., numpy.newaxis]
    new_arr = numpy.repeat(mean_arr3d[:, :, :], 3, axis=2)
    return pygame.surfarray.make_surface(new_arr)


def fade(surface, percentage):
    arr = pygame.surfarray.pixels3d(surface)
    factor = percentage / 100
    fade = arr * factor
    return pygame.surfarray.make_surface(fade)

