import pygame

import globals as g
from timeline_logger import timeline_logger
from spritesheet import SpriteSheet


class Spark(pygame.sprite.Sprite):

    current_id = 0

    def __init__(self, path, edge, speed=g.DEFAULT_SPARK_SPEED):
        super().__init__()

        self.id = Spark.current_id
        Spark.current_id += 1

        self._path = path
        self._edge = edge
        self._speed = speed
        
        self.rect = pygame.Rect(0, 0, g.SPARK_SIZE.x, g.SPARK_SIZE.y)
        self.rect.center = g.loc_to_pos(self._edge.from_node)

        self._initialising = True


    @property
    def hitbox(self):
        offset = (g.SPARK_SIZE - g.SPARK_HITBOX_SIZE) / 2
        topleft = self.rect.topleft + offset
        return pygame.Rect(topleft, g.SPARK_HITBOX_SIZE)

   
    def update(self, cycle, level, audio):

        # don't move on the cycle the spark spawns in
        if(self._initialising == True):
            loc = g.pos_to_loc(self.rect.center)
            timeline_logger.log(f"spark{self.id}: init at: {self.rect.center}/{loc}", cycle)
            self._initialising = False
            return

        # update screen position (one of direction.x or direction.y will always be 0)
        advance_info = self._path.advance_position(self.rect.center, self._edge, self._speed)

        self.rect.center = advance_info["position"]
        self.direction = advance_info["direction"]
        new_edge = advance_info["edge"]

        if g.LOG_SPARK_MOVEMENT:
            # has the spark moved onto an new edge?
            if advance_info["edge"] != self._edge:
                timeline_logger.log(f"spark{self.id}: MOVETO: {self.rect.center} edge was:{self._edge} is now:{new_edge}", cycle)
            else:
                timeline_logger.log(f"spark{self.id}: moveto: {self.rect.center}", cycle)

        self._edge = new_edge

        # check for collisions with emitters
        for emitter in level.emitters:
            if emitter.playing() == False:
                if emitter.hitbox.colliderect(self.hitbox):
                    emitter.play(audio)


    def draw(self, surface):        
        pygame.draw.polygon(surface, "blue", [self.rect.midtop, self.rect.midright, self.rect.midbottom, self.rect.midleft])

        if g.DEBUG_SHOW_HITBOXES:
            pygame.draw.rect(surface, "yellow", self.hitbox)

    
    def get_current_position():
        return (self.rect.x, self.rect.y)
