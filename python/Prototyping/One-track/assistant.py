from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState


class Assistant(pygame.sprite.Sprite):

    def __init__(self, assistant_type, position, colour, shadow_colour):
        super().__init__()

        self.type = assistant_type
        self.emitter_type = EmitterType(self.type.value)
        self.colour = colour
        self.shadow_colour = shadow_colour
        # anchored_location will only be set after the assistant is anchored
        self.anchored_location = None
        self.highlight = False

        # build the shape
        # node format:
        # (x_off, y_off) - from root node; defined in grid coords
        # (exit north, exit south, exit east, exit west) - path definition
        if self.type == AssistantType.KICK_EMITTER:            
            self.nodes = {(0,0):(1,1,0,0), (0, 1):(1,0,0,0), (0,-1):(0,1,0,0)}
        if self.type == AssistantType.BASS_EMITTER:
            self.nodes = {(0, 0):(1,1,1,1), 
                          (0, 1):(1,1,0,0),
                          (0, 2):(1,1,0,0),
                          (0, 3):(1,0,1,0),
                          (1, 3):(0,0,1,1),
                          (2, 3):(0,0,1,1),
                          (3, 3):(1,0,0,1),
                          (3, 2):(1,1,0,0),
                          (3, 1):(1,1,0,0),
                          (1, 0):(0,0,1,1),
                          (2, 0):(0,0,1,1),
                          (3, 0):(0,1,0,1),
                          (0,-1):(0,1,0,0),
                          (-1,0):(0,0,1,0)}

        self.build_surface()                
        self.update(position)
        self.redraw(self.shadow_colour)


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
        self.rootnode_offset = (0 - extents["max_minus_x"], 0 - extents["max_minus_y"])
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()


    def rotate(self):
        # remember the current root position for later
        root_topleft = self.get_root_topleft()

        # rotation is clockwise
        # rotation works by exchanging x and y coords and then inverting the new y
        rotated_nodes = {}
        for node, exits in self.nodes.items():
            rotated_node = (node[1], 0 - node[0])
            rotated_exits = (exits[2], exits[3], exits[1], exits[0])
            rotated_nodes[rotated_node] = rotated_exits
        self.nodes = rotated_nodes
        print(f"assistant.rotate - nodes:{self.nodes}")

        self.build_surface()
        print(f"assistant.rotate - updating: topleft{root_topleft}")
        self.update(root_topleft)

        
    def update(self, topleft):
        self.rect.x = x(topleft) - x(self.rootnode_offset) * TILE_SIZE
        self.rect.y = y(topleft) - y(self.rootnode_offset) * TILE_SIZE


    def get_root_topleft(self):
        return grid_to_screen(self.get_root_location())


    def get_root_location(self):
        if self.anchored_location is not None:
            return self.anchored_location

        location = screen_to_grid(self.rect.topleft)
        root_location = (x(location) + x(self.rootnode_offset), y(location) + y(self.rootnode_offset))
        log(4, "Assistant.get_root_location: location (rect) = {}, root_location = {}".format(location, root_location))
        return root_location


    def get_node_locations(self):
        node_locations = []
        root_location = self.get_root_location()
        for node_offset in self.nodes.keys():
            node_locations.append((x(root_location) + x(node_offset), 
                                   y(root_location) + y(node_offset)))

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


    def get_exits(self, position):
        requested_location = screen_to_grid(position)

        # which node is the requested location in?
        for offset in self.nodes.keys():
            if (x(self.anchored_location) + x(offset), y(self.anchored_location) + y(offset)) == requested_location:
                return self.nodes[offset]
            
        return (0,0,0,0)


    def redraw(self, colour=None):
        if colour == None: colour = self.colour
        for node in self.nodes.keys():
            rect = pygame.Rect((x(node) + x(self.rootnode_offset)) * TILE_SIZE,
                               (y(node) + y(self.rootnode_offset)) * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.image, colour, rect, border_radius=3)
            if self.highlight:
                pygame.draw.rect(self.image, "white", rect, 3, border_radius=3)
                                                  

    def __repr__(self):
        repr = "Assistant(type={}\n    emitter_type={}\n".format(self.type, self.emitter_type)
        repr = repr + "    colour={}\n    shadow_colour={}\n".format(self.colour, self.shadow_colour)
        repr = repr + "    nodes={}\n    rootnode_offset={})".format(self.nodes,self.rootnode_offset)

        return repr    

