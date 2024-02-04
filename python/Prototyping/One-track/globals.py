import pygame
from level_data import level_map

TILE_SIZE = 32

SCREEN_WIDTH = 640
SCREEN_HEIGHT = len(level_map) * TILE_SIZE

BEATBUG_SIZE = 16

H_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2
V_CENTER_BEATBUG = (TILE_SIZE - BEATBUG_SIZE) / 2

SPAWN_TIMER_EVENT = pygame.USEREVENT + 1

def x(coords):
  return coords[0]

def y(coords):
  return coords[1]  

def grid_to_screen(location):
  return (location[0] * TILE_SIZE, location[1] * TILE_SIZE)
  
def screen_to_grid(position):
  return (int(position[0] / TILE_SIZE), int(position[1] / TILE_SIZE))
  
def get_containing_grid(position):
  left = x(position) - x(position) % TILE_SIZE
  top = y(position) - y(position) % TILE_SIZE
  return (left, top)

def get_grid_rect(location):
  position = grid_to_screen(location)
  return pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
  
def get_grid_cell_data(location):
  row = level_map[location[1]]
  cell = row[location[0]]
  return cell
  
def get_direction_vector(bearing):
  if bearing == 'N' or bearing == 'O':
    return pygame.math.Vector2(0,-1)
  elif bearing == 'S':
    return pygame.math.Vector2(0,1)
  elif bearing == 'W':
    return pygame.math.Vector2(-1,0)
  elif bearing == 'E':  
    return pygame.math.Vector2(1,0)
    
  return pygame.math.Vector2(0,0)

  
def add_tuples(tup1, tup2):
  return tuple(map(lambda i, j: i + j, tup1, tup2))