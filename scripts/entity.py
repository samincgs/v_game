import pygame
import math
import random

from .config import config
from .utils import outline, clip
from .spark import CurvedSpark

class Entity:
    def __init__(self, game, pos, size, e_type):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.max_health = config['entities'][e_type]['base_health'] if self.type in config['entities'] else 0
        self.health = self.max_health
        self.flip = [False, False]
        self.hurt = 0
        self.active_animation = None
        self.dead = False
        self.drops = []
                
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
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    @property
    def center(self):
        return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2] 
            
    def set_action(self, action_id, force=False):
        if force:
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id)
        elif (not self.active_animation) or (self.active_animation.id != self.type + '_' + action_id):
            self.active_animation = self.game.assets.animations.new(self.type + '_' + action_id)

    def damage(self, amt):
        self.health -= amt
        if self.health <= 0:
            self.die()
        if self.type in self.type in config['entities']:
            self.hurt = 1
        return self.dead
        
        
    def die(self): 
        self.dead = True
        
        size = 4
        entity_img = self.img.copy()
        
        for y in range(entity_img.get_height() // size + 1):
            for x in range(entity_img.get_width() // size + 1):
                particle_img = clip(entity_img, (x * size, y * size), (size, size))
                self.game.world.particle_manager.add_death_particle(self.game, particle_img, self.center.copy(), 0, random.randint(300, 500), 0.9, [random.randint(0, 150) - 75, random.randint(0, 100) - 125], duration=2)
        
        # create death sparks
        for i in range(16):
            angle = i / 8 * math.pi
            self.game.world.spark_manager.sparks.append(CurvedSpark(self.center.copy(), angle + random.random() / 5, speed=random.random() * 2 + 1, curve=0, scale=4, decay_rate=0.08))
            
        for item_drop in self.drops:
            self.game.world.entities.drop_item(self.pos.copy(), (1, 1), item_drop, velocity=(random.randint(0, 320) - 150, random.randint(0, 20) - 200))

    def get_angle(self, target):
        if isinstance(target, Entity):
            return math.atan2(target.center[1] - self.center[1], target.center[0] - self.center[0])
        else:
            return math.atan2(target[1] - self.pos[1], target[0] - self.pos[0])
    
    def get_distance(self, target): # order of x, y doesnt matter because it calculates a linear distance and is being squared
        if isinstance(target, Entity):
            return math.sqrt((target.pos[0] - self.pos[0]) ** 2 + (target.pos[1] - self.pos[1]) ** 2)
        else:
            return math.sqrt((target[0] - self.pos[0]) ** 2 + (target[1] - self.pos[1]) ** 2)
    
    def in_range(self, target, radius):
        return self.get_distance(target) <= radius
    
    
    def gen_mask(self, img, setcolor, unsetcolor=(0, 0, 0, 0)):
        temp_mask = pygame.mask.from_surface(img)
        mask_img = temp_mask.to_surface(setcolor=setcolor, unsetcolor=unsetcolor)
        return mask_img
    
    def collisions(self, tilemap, movement=(0, 0)):
        directions = {d: False for d in ['top', 'right', 'left', 'bottom']}
                
        # horizontal
        self.pos[0] += movement[0]
        tiles = tilemap.get_nearby_rects(self.center)
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
        tiles = tilemap.get_nearby_rects(self.center)
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
            offset[0] += self.active_animation.config['offset'][0]
            offset[1] += self.active_animation.config['offset'][1]
        return offset
    
    def render(self, surf, offset=(0, 0)):
        offset = self.calculate_render_offset(offset=offset)
        if self.active_animation.config['outline']:
            outline(surf, self.img, loc=(self.pos[0] - offset[0], self.pos[1] - offset[1]), color=self.active_animation.config['outline'])
        surf.blit(self.img, (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1]))) 
        if self.hurt:
            mask_img = self.gen_mask(self.img, setcolor=(255, 255, 255, int(self.hurt * 255)))
            surf.blit(mask_img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        
    def update(self, dt):
        if self.active_animation:
            self.active_animation.play(dt)
        if self.hurt:
            self.hurt = max(0, self.hurt - dt * 2)
        return self.dead

        