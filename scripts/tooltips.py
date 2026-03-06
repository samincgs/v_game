import pygame

import scripts.pgtools as pt

from .itemdrop import Itemdrop
from .portal import Portal

INTERACTABLE_ENTITIES = [Itemdrop, Portal]


def lerp(a, b, t):
    return a + (b - a) * t

class Tooltips:
    def __init__(self, game):
        self.game = game
        
        self.closest_entity = None
        self.prev_entity = None
        self.font = self.game.assets.fonts['small_white']
        
        self.tooltip_time = 0
        self.tooltip_target = 20
        self.tooltip_speed = 200
        self.tooltip_phase = 0 # 0 = idle, 1 = growing, 2 = shrinking
        
        
    
    def update(self, dt):
        all_interactable_entities = [entity for entity in self.game.world.entities.items + self.game.world.entities.entities if (isinstance(entity, Itemdrop) or isinstance(entity, Portal))] #TODO: adapt to INTERACTABLE_ENTITIES
        
        player = self.game.world.player
        self.closest_entity = min([entity for entity in all_interactable_entities if player.in_range(entity.pos, 20)], key=lambda entity: pt.utils.get_distance(player.pos, entity.pos), default=None)

        if self.closest_entity != self.prev_entity:
            self.tooltip_time = 0
            self.tooltip_phase = 1
            self.prev_entity = self.closest_entity
            
        if self.tooltip_phase == 1:
            self.tooltip_time = min(self.tooltip_target, self.tooltip_time + self.tooltip_speed * dt)
            if self.tooltip_time >= self.tooltip_target:
                self.tooltip_phase = 2
        elif self.tooltip_phase == 2:
            self.tooltip_time = max(0, self.tooltip_time - self.tooltip_speed * dt)     
            if self.tooltip_time <= 0:
                self.tooltip_phase = 0   
        
        
        # item pickup
        if self.closest_entity:
            if self.game.input.pressing('interact'):
                if self.closest_entity.type == 'item' or self.closest_entity.type.split('_')[0] == 'item':
                    player.pickup_item(self.closest_entity)
            
                
                

    def render(self, surf, offset=(0, 0)):
        if self.closest_entity:
            name = self.closest_entity.category
            
            x = self.closest_entity.center[0] - offset[0]
            y = self.closest_entity.center[1] - offset[1]
            

            points = [(x, y - 8), (x + 6, y - 14), (x + 6 + self.font.get_width(name) + 6 + self.tooltip_time, y - 14)]
            pygame.draw.lines(surf, (255, 255, 255), closed=False, points=points)
            self.font.render(surf, name, (x + 9, y - 23 - self.tooltip_time / 6))