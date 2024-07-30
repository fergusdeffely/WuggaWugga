from enum import Enum
import pygame
import pygame_gui
from globals import *

class AssistantType(Enum):
    PATH = 1


class Assistant(pygame.sprite.Sprite):

    def __init__(self, assistant_type, emit_sound, nodes, colour, shadow_colour, speed, location=None):
        super().__init__()

        self.type = assistant_type
        self.emit_sound = emit_sound
        self.colour = colour
        self.shadow_colour = shadow_colour
        self.speed = speed
        self.nodes = nodes
        self.location = location
        self.anchored = False
        self.highlight = False
        self.rootnode_offset = pygame.Vector2(0, 0)

        self.build_surface()
        self.rect.x -= self.rootnode_offset.x * TILE_SIZE
        self.rect.y -= self.rootnode_offset.y * TILE_SIZE
        self.redraw(self.shadow_colour)


    @property
    def anchored_location(self):
        if self.anchored == True:
            return self.location
        
        return None


    @property
    def ui_object_id(self):
        return "#{}".format(self.colour)


    def build_surface(self):
        extents = self.get_node_extents()

        width = (extents["max_plus_x"] - extents["max_minus_x"]) * TILE_SIZE + TILE_SIZE
        height = (extents["max_plus_y"] - extents["max_minus_y"]) * TILE_SIZE + TILE_SIZE

        '''
        Take the case where we have an assistant that looks like the following:
               O
               O
               OOXOO
                   O
                   O
        It will be convenient when rotating to have the root node in the centre -
        that is at X - and to have the other nodes defined in relative terms.

        To facilitate drawing, we keep an offset to the root in grid coords.
        In the example above the root offset would be (2,2)
        '''
        self.rootnode_offset = pygame.Vector2(-extents["max_minus_x"], -extents["max_minus_y"])
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()


    def rotate(self, level_offset):
        # remember the current root position for later
        root_topleft = grid_to_screen(self.location, level_offset)

        # rotation is clockwise
        # rotation works by exchanging x and y coords and then inverting the new y
        rotated_nodes = {}
        for node, exits in self.nodes.items():
            rotated_node = (node[1], -node[0])
            rotated_exits = (exits[2], exits[3], exits[1], exits[0])
            rotated_nodes[rotated_node] = rotated_exits
        self.nodes = rotated_nodes
        print(f"assistant.rotate - nodes:{self.nodes}")

        self.build_surface()
        print(f"assistant.rotate - updating: topleft{root_topleft}")
        self.update(root_topleft, level_offset)

        
    def update(self, topleft, level_offset):
        # self.location is always the root node location
        self.location = screen_to_grid(topleft, level_offset)
        self.rect.x = x(topleft) - self.rootnode_offset.x * TILE_SIZE
        self.rect.y = y(topleft) - self.rootnode_offset.y * TILE_SIZE


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def get_node_locations(self):
        node_locations = []
        for node_offset in self.nodes.keys():
            node_locations.append(pygame.Vector2(self.location.x + x(node_offset), 
                                                 self.location.y + y(node_offset)))

        log(4, f"Assistant.get_node_locations: returning: {node_locations}")
        return node_locations
        

    def has_node(self, location):
        for node_location in self.get_node_locations():
            if location == node_location:
                return True

        return False        


    def get_node_extents(self):
        max_plus_x = 0
        max_minus_x = 0
        max_plus_y = 0
        max_minus_y = 0        
        
        for node in self.nodes.keys():
            if node[0] > max_plus_x:
                max_plus_x = node[0]
            if node[0] < max_minus_x:
                max_minus_x = node[0]
            if node[1] > max_plus_y:
                max_plus_y = node[1]
            if node[1] < max_minus_y:
                max_minus_y = node[1]

        return {"max_plus_x": max_plus_x, 
                "max_minus_x": max_minus_x, 
                "max_plus_y": max_plus_y, 
                "max_minus_y": max_minus_y}


    def get_exits(self, position, level_offset):
        requested_location = screen_to_grid(position, level_offset)

        # is the requested location one of the nodes?
        for node_offset in self.nodes.keys():
            if (self.location.x + node_offset[0], self.location.y + node_offset[1]) == requested_location:
                return self.nodes[node_offset]
            
        return (0,0,0,0)


    def redraw(self, colour=None):        
        if colour == None: 
            colour = self.colour

        for node in self.nodes.keys():
            rect = pygame.Rect((node[0] + self.rootnode_offset.x) * TILE_SIZE,
                               (node[1] + self.rootnode_offset.y) * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.image, colour, rect, border_radius=3)
            if self.highlight:
                pygame.draw.rect(self.image, "white", rect, 3, border_radius=3)


    def __repr__(self):
        repr = f"Assistant:type={self.type}\n    emit_sound={self.emit_sound}\n"
        repr = repr + f"    colour={self.colour}\n    shadow_colour={self.shadow_colour}\n"
        repr = repr + f"    nodes={self.nodes}\n    rootnode_offset={self.rootnode_offset}"
        repr = repr + f"    anchored={self.anchored}\n    highlight={self.highlight}"

        return repr    

