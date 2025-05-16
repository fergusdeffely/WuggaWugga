import pygame
import pygame_gui
import globals as g
from timeline_event import TimelineEvent
from directed_graph import GraphEdge, DirectedGraph
from spark import Spark


class Path():

    def __init__(self, path_name, config_data, timeline):

        self._graph = None
        self._sparks = pygame.sprite.Group()
        self._parse_config(path_name, config_data, timeline)


    def _parse_config(self, path_name, config_data, timeline):
        node_data = config_data.get("nodes", None)

        self._graph = DirectedGraph(node_data)
        if config_data["sparks"]:
            for name, spark_data in config_data["sparks"].items():
                speed = spark_data.get("speed", g.DEFAULT_SPARK_SPEED)
                node_location_text = spark_data.get("node", None)
                start_node = g.parse_location_text(node_location_text)
                edge = self._graph.get_edge(start_node)
                self._sparks.add(Spark(self, edge, speed))


    def advance_position(self, position, edge, speed):
        # advances a position on a path, given a current position, an edge
        # and the speed to move at

        direction = edge.get_normalised_direction()
        new_direction = direction
        new_edge = edge

        # calc new position (one of direction.x or direction.y will always be 0)
        delta_x = direction.x * speed
        delta_y = direction.y * speed
        new_x = position[0] + delta_x
        new_y = position[1] + delta_y
        edge_end_pos = g.loc_to_pos(edge.to_node)

        if new_x * direction.x > edge_end_pos[0] * direction.x:
            # have passed the end of the current edge
            new_x = edge_end_pos[0]
            new_edge = self._graph.get_edge(edge.to_node)
            new_direction = new_edge.get_normalised_direction()

            remainder_x = abs(delta_x - (edge_end_pos[0] - position[0]))
            # we've either turned north or south, so apply the remainder to the y component
            new_y = edge_end_pos[1] + remainder_x * new_direction[1]

        elif new_y * direction.y > edge_end_pos[1] * direction.y:
            # have passed the end of the current edge
            new_y = edge_end_pos[1]
            new_edge = self._graph.get_edge(edge.to_node)
            new_direction = new_edge.get_normalised_direction()

            remainder_y = abs(delta_y - (edge_end_pos[1] - position[1]))
            # we've either turned east or west, so apply the remainder to the x component
            new_x = edge_end_pos[0] + remainder_y * new_direction[0]

        # return edge, position and direction
        return {"edge": new_edge, "position": (new_x, new_y), "direction": new_direction}


    def update(self, cycle, level, audio):
        for spark in self._sparks:
           spark.update(cycle, level, audio)


    def draw(self, surface):
        for edge in self._graph.get_edges():
            self.draw_edge(surface, edge)


    def draw_sparks(self, surface):
        for spark in self._sparks:
            spark.draw(surface)


    def draw_edge(self, surface, edge):
        from_pos = g.loc_to_pos(pygame.Vector2(edge.from_node))
        to_pos = g.loc_to_pos(pygame.Vector2(edge.to_node))
        pygame.draw.line(surface, "gray", from_pos, to_pos)
        x = g.x(from_pos) - g.PATHNODE_SIZE.x / 2
        y = g.y(from_pos) - g.PATHNODE_SIZE.y / 2
        node_rect = pygame.Rect((x, y), g.PATHNODE_SIZE)
        pygame.draw.rect(surface, "gray", node_rect)
