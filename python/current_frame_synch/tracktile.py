import pygame
from tile import Tile

class TrackTile(Tile):

    def __init__(self, tile_location, tile_data, grid_offset):
        super().__init__(tile_location, grid_offset)
        self._parse_tracktile_config(tile_data)


    def _parse_tracktile_config(self, tile_data):
        self.exits = tile_data["exits"]
        self.info = tile_data.get("info")


    def __repr__(self):
        return f"TrackTile: rect: {self.rect} exits:{self.exits} info:{self.info}"
