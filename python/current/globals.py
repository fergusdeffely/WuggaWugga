import pygame
import pygame_gui
from enums import *

LOGGING_LEVEL = 4
LOG_FRAME_DELTAS = False
LOG_BUG_MOVEMENT = True

NULL_LOCATION = (None, None)
TILE_SIZE = 32

SCREEN_WIDTH_TILES = 32
SCREEN_HEIGHT_TILES = 16
SCREEN_WIDTH_PIXELS = SCREEN_WIDTH_TILES * TILE_SIZE
SCREEN_HEIGHT_PIXELS = SCREEN_HEIGHT_TILES * TILE_SIZE
SCREEN_SIZE = (SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS)
DRAW_GRID = True

BEATBUG_SIZE = 16
BEATBUG_SPEED = TILE_SIZE * 2
EMITTER_SPEED = TILE_SIZE

H_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2
V_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2

VECTOR_NORTH = pygame.Vector2(0,-1)
VECTOR_SOUTH = pygame.Vector2(0, 1)
VECTOR_EAST  = pygame.Vector2(1, 0)
VECTOR_WEST  = pygame.Vector2(-1,0)

FONT_SIZE = 16
INFO_TEXT_OFFSET = pygame.Vector2(0, 0 - TILE_SIZE * 3 / 4)

BEATBUG_SPAWN_TIMER_DURATION = 2000

BASE_WUGGA_USEREVENT = pygame_gui.UI_TEXT_EFFECT_FINISHED + 1
CHANNEL_READY_EVENT = BASE_WUGGA_USEREVENT + 0

ASSISTANT_BUTTON_SPACER = TILE_SIZE / 2

class SuspendAction(Enum):
    ENTERED = 0
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

def grid_to_screen(location, level_offset):
    return ((location.x + level_offset.x) * TILE_SIZE, 
            (location.y + level_offset.y) * TILE_SIZE)

def screen_to_grid(position, level_offset):
    return pygame.Vector2(int(position[0] / TILE_SIZE) - level_offset.x, 
                          int(position[1] / TILE_SIZE) - level_offset.y)

def get_tile_topleft(position):
    left = position[0] - position[0] % TILE_SIZE
    top = position[1] - position[1] % TILE_SIZE
    return (left, top)

def get_tile_rect(location, level_offset):
    topleft = grid_to_screen(location, level_offset)
    return pygame.Rect(x(topleft), y(topleft), TILE_SIZE, TILE_SIZE)
  
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
  
def add_tuples(tup1, tup2):
    return tuple(map(lambda i, j: i + j, tup1, tup2))

def log(level, message):
    if level <= LOGGING_LEVEL:
        print(message)

def get_html_colour(colour):
    return f"#{colour.r:02x}{colour.g:02x}{colour.b:02x}"