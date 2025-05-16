from enum import Enum
import pygame
import pygame_gui
import globals as g

class AssistantType(Enum):
    PATH = 1


class Assistant(pygame.sprite.Sprite):

    def __init__(self, name, json, location=None):
        super().__init__()

        self.name = name
        self._parse_config(json)
        self.location = location
        self.anchored = False
        self.highlight = False
        self.rootnode_offset = pygame.Vector2(0, 0)

        self.build_surface()
        self.rect.x -= self.rootnode_offset.x * g.GRID_SIZE
        self.rect.y -= self.rootnode_offset.y * g.GRID_SIZE
        self.redraw(self.shadow_colour)


    def _parse_config(self, json):
        if json["type"] == "path":
            self.type =  AssistantType.PATH
        else:
            self.type = None        
        self.emit_sound = json["emit_sound"]
        self.play_duration = json["play_duration"]
        self.colour = pygame.Color(json["colour"])
        self.shadow_colour = pygame.Color(json["shadow_colour"])
        # lower the alpha for the shadow colour
        self.shadow_colour[3] = 150
        self.speed = json["speed"]
        self.nodes = {}
        for node_text, exits in json["nodes"].items():
            node = g.parse_location_text(node_text)
            self.nodes[node] = exits
          

    def build_surface(self):
        extents = self.get_extents()

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

        width = (extents["max_plus_x"] - extents["max_minus_x"]) * g.GRID_SIZE + g.GRID_SIZE
        height = (extents["max_plus_y"] - extents["max_minus_y"]) * g.GRID_SIZE + g.GRID_SIZE

        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()


    def rotate(self):
        # remember the current root position for later
        position = g.loc_to_pos(self.location)

        # rotation is clockwise
        # rotation works by exchanging x and y coords and then negating the new y
        rotated_nodes = {}
        for node, exits in self.nodes.items():
            rotated_node = (node[1], -node[0])
            rotated_exits = (exits[2], exits[3], exits[1], exits[0])
            rotated_nodes[rotated_node] = rotated_exits
        self.nodes = rotated_nodes
        g.log(4, f"assistant.rotate - nodes:{self.nodes}")

        # rebuild the surface after changes
        self.build_surface()

        g.log(4, f"assistant.rotate - updating: {position}")
        self.update(position)

        
    def update(self, position):
        # position specifies the topleft of the current grid location of the rootnode
        self.location = g.pos_to_loc(position)

        # adjust the containing rect relative to the root node locatoin
        self.rect.left = g.x(position) - self.rootnode_offset.x * g.GRID_SIZE
        self.rect.top = g.y(position) - self.rootnode_offset.y * g.GRID_SIZE


    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def get_node_locations(self):
        node_locations = []
        for node_offset in self.nodes.keys():
            node_locations.append(pygame.Vector2(self.location.x + g.x(node_offset), 
                                                 self.location.y + g.y(node_offset)))

        g.log(4, f"Assistant.get_node_locations: returning: {node_locations}")
        return node_locations
        

    def has_node(self, location):
        for node_location in self.get_node_locations():
            if location == node_location:
                return True

        return False        


    def get_extents(self):
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
        requested_location = pos_to_loc(position)

        # is the requested location one of the nodes?
        for node_offset in self.nodes.keys():
            if (self.location.x + node_offset[0], self.location.y + node_offset[1]) == requested_location:
                return self.nodes[node_offset]
            
        return (0,0,0,0)


    def redraw(self, colour=None):        
        if colour == None: 
            colour = self.colour

        for node in self.nodes.keys():
            rect = pygame.Rect((node[0] + self.rootnode_offset.x) * g.GRID_SIZE,
                               (node[1] + self.rootnode_offset.y) * g.GRID_SIZE,
                               g.GRID_SIZE, g.GRID_SIZE)
            pygame.draw.rect(self.image, colour, rect, border_radius=3)
            if self.highlight:
                pygame.draw.rect(self.image, "white", rect, 3, border_radius=3)


    def __repr__(self):
        repr = f"Assistant:type={self.type}\n    emit_sound={self.emit_sound}\n"
        repr = repr + f"    colour={self.colour}\n    shadow_colour={self.shadow_colour}\n"
        repr = repr + f"    nodes={self.nodes}\n    rootnode_offset={self.rootnode_offset}\n"
        repr = repr + f"    anchored={self.anchored}\n    highlight={self.highlight}\n"
        repr = repr + f"    speed={self.speed}"
        return repr    

