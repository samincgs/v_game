import math
import pygame

class Camera:
    def __init__(self, display_size, tile_size=16, lag=20):
        self.display_size = display_size
        self.tile_size = tile_size
        self.lag = lag
        
        self.targeted_entity = None
        self.targeted_pos = None
        self.scroll = [0, 0]

    @property
    def pos(self):
        return (int(self.scroll[0]), int(self.scroll[1]))
    
    @property
    def float_pos(self):
        return self.scroll

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.display_size[0], self.display_size[1])
    
    @property
    def entity_location(self):
        if self.targeted_entity:
            loc = (self.targeted_entity.center[0] - self.display_size[0] // 2, self.targeted_entity.center[1] - self.display_size[1] // 2)
        if self.targeted_pos:
            loc = (self.targeted_pos[0] - self.display_size[0] // 2, self.targeted_pos[1] - self.display_size[1] // 2)
        return loc
    
    @property
    def target(self):
        return self.entity_location
    
    @property
    def get_visible_screen(self):
        return (int((self.pos[0] + self.display_size[0]) // self.tile_size) + 1), (int((self.pos[1] + self.display_size[1]) // self.tile_size) + 1)
        
    def follow_target(self, val, target, lag):
        val += (target - val) / lag 
        return val

    def set_target(self, target, snap=False):
        if hasattr(target, 'center'):
            self.targeted_entity = target
        else:
            self.targeted_pos = target
        if snap:
            self.snap_to_target()

        
    def snap_to_target(self):
        self.scroll[0] = self.target[0]
        self.scroll[1] = self.target[1]
    
    def update(self):
        if self.targeted_entity or self.targeted_pos:
            target = self.target
            self.scroll[0] = self.follow_target(self.scroll[0], target[0], self.lag)
            self.scroll[1] = self.follow_target(self.scroll[1], target[1], self.lag)
            
        