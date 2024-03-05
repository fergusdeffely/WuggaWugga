import pygame
import pygame_gui
from enums import *
from level_data import level_map

LOGGING_LEVEL = 1
LOG_FRAME_DELTAS = False
LOG_BUG_MOVEMENT = True

NULL_LOCATION = (None, None)
TILE_SIZE = 32
 
SCREEN_WIDTH = len(level_map[0]) * TILE_SIZE
SCREEN_HEIGHT = len(level_map) * TILE_SIZE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DRAW_GRID = True

BEATBUG_SIZE = 16
BEATBUG_SPEED = TILE_SIZE * 2
EMITTER_SPEED = TILE_SIZE

H_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2
V_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2

FONT_SIZE = 16
COUNTDOWN_HEIGHT = FONT_SIZE
COUNTDOWN_WIDTH = FONT_SIZE * 3

SPAWN_TIMER_DURATION = 2000

BASE_WUGGA_USEREVENT = pygame_gui.UI_TEXT_EFFECT_FINISHED + 1

CHANNEL_READY_EVENT = BASE_WUGGA_USEREVENT + 0

ASSISTANT_ROSTER = [("red", AssistantType.KICK_EMITTER),
                    ("yellow", AssistantType.BASS_EMITTER)]

ASSISTANT_BUTTON_SPACER = TILE_SIZE / 2

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

def grid_to_screen(location):
    return (location[0] * TILE_SIZE, location[1] * TILE_SIZE)
  
def screen_to_grid(position):
    return (int(position[0] / TILE_SIZE), int(position[1] / TILE_SIZE))

def get_tile_topleft(position):
    left = x(position) - x(position) % TILE_SIZE
    top = y(position) - y(position) % TILE_SIZE
    return (left, top)

def get_tile_rect(location):
    topleft = grid_to_screen(location)
    return pygame.Rect(x(topleft), y(topleft), TILE_SIZE, TILE_SIZE)
  
def get_grid_cell_data(location):
    row = level_map[location[1]]
    cell = row[location[0]]
    return cell
  
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