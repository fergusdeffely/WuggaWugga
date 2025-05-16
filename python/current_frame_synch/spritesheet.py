import pygame


class SpriteSheet:

    def __init__(self, filename, offset_x, offset_y, tiles_x, tiles_y, tile_width, tile_height, color_key = None):
        self._tile_sheet = pygame.image.load(filename)
        self.current_image = pygame.Surface((tile_width, tile_height))
        if color_key:
            self._tile_sheet = self._tile_sheet.convert()
            self._tile_sheet.set_colorkey(color_key)
            self.current_image = self.current_image.convert()
            self.current_image.set_colorkey(color_key)

        else:
            self._tile_sheet = self._tile_sheet.convert_alpha()
            self.current_image = self.current_image.convert_alpha()
            
        self._tile_sheet_cells = {}
        self._animations = {"all":[]}
        for y in range(tiles_y):
            self._tile_sheet_cells[y] = []
            for x in range(tiles_x):
                rect = pygame.Rect (offset_x + tile_width * x,
                       offset_y + tile_height * y,
                       tile_width,
                       tile_height)

                self._tile_sheet_cells[(x,y)] = rect 
                self._animations["all"].append(rect)

        self._current_animation = None
        self._animation_step = 1
        self._frame_count = 0
        

    def register_animation(self, name, cell_list):
        tile_rects = [self._tile_sheet_cells[cell] for cell in cell_list]
        self._animations[name] = tile_rects


    def play_animation(self, name, step=1, index=0):
        self._current_animation = self._animations[name]
        self._animation_step = step
        self._index = index
        self._frame_count = 0


    def update(self):
        if self._current_animation is not None:
            if self._frame_count % self._animation_step == 0:
                # update index with looping
                self._index = (self._index + 1) % len(self._current_animation)
                tile_rect = self._current_animation[self._index]
                self.current_image.blit(self._tile_sheet, self.current_image.get_rect(), area=tile_rect)
                
            self._frame_count += 1

        return self.current_image

    def draw(self, surface, x, y):
        if self._current_animation is not None:
            tile_rect = self._current_animation[self._index]
            surface.blit(self._tile_sheet, dest=(x,y), area=tile_rect)
