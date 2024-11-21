import pygame
import math

from .config import config
from .utils import outline

class Entity:
    def __init__(self, game, pos, size, e_type):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        
        self.max_health = 1
        if self.type in config['entities']:
            self.max_health = config['entities'][e_type]['base_health']
        self.health = self.max_health
        self.flip = [False, False]
        self.hurt = 0
        self.centered = False
        self.active_animation = None
        
        if self.type + '_idle' in self.game.assets.animations.animations:
            self.set_action('idle')
            
    @property 
    def img(self):
        if self.active_animation:
            img = self.active_animation.img
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        return img
    
    @property
    def rect(self):
        if not self.centered:
            return pygame.Rect(int(self.pos[0]), int(self.pos[1]), self.size[0], self.size[1])
        else:
            return pygame.Rect(int(self.pos[0] - self.size[0] // 2), int(self.pos[1] - self.size[1] // 2), self.size[0], self.size[1])
    
    @property
    def center(self):
        if self.centered:
            return self.pos.copy()
        else:
            return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2] 
        
    def set_action(self, action_id, force=False):
        if force:
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id)
        elif (not self.active_animation) or (self.active_animation.data.id != self.type + '_' + action_id):
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id)

    def get_angle(self, target):
        # if isinstance(target, Entity):
        return math.atan2(target.center[1] - self.center[1], target.center[0] - self.center[0])
        # else:
        #     return math.atan2(target.pos[1] - self.pos[1], target.pos[0] - self.pos[0])
    
    def get_distance(self, target): # order of x, y doesnt matter because it calculates a linear distance and is being squared
        return math.sqrt((target.pos[0] - self.pos[0]) ** 2 + (target.pos[1] - self.pos[1]) ** 2)
    
    def in_range(self, target, radius):
        return self.get_distance(target) <= radius
    
    def collisions(self, tilemap, movement=(0, 0)):
        directions = {d: False for d in ['top', 'right', 'left', 'bottom']}
        
        # horizontal
        self.pos[0] += movement[0]
        tiles = tilemap.get_nearby_rects(self.pos)
        hit_list = tilemap.collision_test(self.rect, tiles)
        temp_rect = self.rect
        
        for tile in hit_list:
            if movement[0] > 0:
                temp_rect.right = tile.left
                directions['right'] = True
            if movement[0] < 0:
                temp_rect.left = tile.right
                directions['left'] = True
            self.pos[0] = temp_rect.x
            
        # vertical
        self.pos[1] += movement[1] 
        tiles = tilemap.get_nearby_rects(self.pos)
        hit_list = tilemap.collision_test(self.rect, tiles)
        temp_rect = self.rect
        
        for tile in hit_list:
            if movement[1] > 0:
                temp_rect.bottom = tile.top
                directions['bottom'] = True
            if movement[1] < 0:
                temp_rect.top = tile.bottom
                directions['top'] = True 
            self.pos[1] = temp_rect.y
            
        return directions
        
    def calculate_render_offset(self, offset=(0, 0)):
        offset = list(offset)
        if self.active_animation:
            offset[0] += self.active_animation.data.config['offset'][0]
            offset[1] += self.active_animation.data.config['offset'][1]
        if self.centered:
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2
        return offset
    
    def render(self, surf, offset=(0, 0)):
        offset = self.calculate_render_offset(offset=offset)
        if self.active_animation.data.config['outline']:
            outline(surf, self.img, (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), color=self.active_animation.data.config['outline'])
        surf.blit(self.img, (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))) # added one to deal with tilemap size (17x16)
          
    def update(self, dt):
        self.active_animation.play(dt)