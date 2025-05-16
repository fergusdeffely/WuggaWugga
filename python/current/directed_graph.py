import pygame
import pygame_gui
import globals as g

class GraphEdge():

    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node


    def get_normalised_direction(self):
        return (pygame.Vector2(self.to_node) - pygame.Vector2(self.from_node)).normalize()


    def __repr__(self):
        return f"GraphEdge(({self.from_node}) -> {self.to_node})"



class DirectedGraph():

    def __init__(self, nodelist):
        self._nodes = {}

        # construct n-1 edges from n nodes
        # e.g. [a, b, c, a] gives [(a,b), (b,c), (c,a)]
        for i, from_node in enumerate(nodelist):
            if i < len(nodelist) - 1:
                # each node goes to the next node in the nodelist
                from_node = g.parse_location_text(from_node)
                to_node = g.parse_location_text(nodelist[i + 1])
                self._nodes[from_node] = [GraphEdge(from_node, to_node)]


    def add_edge(self, from_node, to_node):
        self._nodes[from_node].append(GraphEdge(from_node, to_node))


    def get_nodes_from(self, node):
        return self._nodes[node]


    def get_edge(self, from_node, index=None):
        if from_node in self._nodes.keys():
            if index is None:
                return self._nodes[from_node][0]
            else:
                return self._nodes[from_node][index]
        return None

    def get_edges(self):
        return [edge
                for edges in self._nodes.values()
                for edge in edges
                ]