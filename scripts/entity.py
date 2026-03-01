import pygame
import math
import random

import scripts.pgtools as pt

from scripts.config import config

class Entity(pt.Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.max_health = config['entities'][e_type]['base_health'] if self.type in config['entities'] else 0
        self.health = self.max_health
        self.hurt = 0
        self.dead = False
        self.drops = []
        self.grass_effect = (0, 0)

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
        
        self.game.window.screenshake = 1.2
        
        for y in range(entity_img.get_height() // size + 1):
            for x in range(entity_img.get_width() // size + 1):
                particle_img = pt.utils.clip(entity_img, (x * size, y * size), (size, size))
                self.game.world.particle_manager.add_death_particle(self.game, particle_img, self.center, 0, random.randint(300, 500), 0.9, [random.randint(0, 150) - 75, random.randint(0, 100) - 125], duration=2)
        
        for i in range(32):
            angle = i / 16 * math.pi
            self.game.world.spark_manager.add_curved_spark(self.center, angle + random.random() / 5, speed=random.random() * 2 + 1, curve=0, scale=4, decay_rate=0.08)
            
        for item_drop in self.drops:
            self.game.world.entities.drop_item(self.pos.copy(), (1, 1), item_drop, velocity=(random.randint(0, 250) - 150, random.randint(0, 20) - 200))
    
    def in_range(self, target, radius):
        return pt.utils.get_distance(self.pos, target) <= radius
    
    def gen_mask(self, img, setcolor, unsetcolor=(0, 0, 0, 0)):
        temp_mask = pygame.mask.from_surface(img)
        mask_img = temp_mask.to_surface(setcolor=setcolor, unsetcolor=unsetcolor)
        return mask_img
    
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        if self.hurt:
            temp_mask = pygame.mask.from_surface(self.img)
            mask_img = temp_mask.to_surface(setcolor=(255, 255, 255, int(self.hurt * 255)), unsetcolor=(0, 0, 0, 0))
            surf.blit(mask_img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def update(self, dt):
        super().update(dt)
        if self.hurt:
            self.hurt = max(0, self.hurt - dt * 2)
        return self.dead

        