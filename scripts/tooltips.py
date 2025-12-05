import pygame

import scripts.pgtools as pt

from .itemdrop import Itemdrop

def lerp(a, b, t):
    return a + (b - a) * t

class Tooltips:
    def __init__(self, game):
        self.game = game
        
        self.items = None  
        self.closest_item = None
        self.prev_item = None
        self.font = self.game.assets.fonts['small_white']
        
        self.tooltip_time = 0
        self.tooltip_target = 20
        self.tooltip_speed = 200
        self.tooltip_phase = 0 # 0 = idle, 1 = growing, 2 = shrinking
        
        
    
    def update(self, dt):
        self.items = [item for item in self.game.world.entities.entities if isinstance(item, Itemdrop)] 
        
        player = self.game.world.player

        self.closest_item = min([item for item in self.items if player.in_range(item.pos, 20)], key=lambda item: pt.utils.get_distance(player.pos, item.pos), default=None)



        if self.closest_item != self.prev_item:
            self.tooltip_time = 0
            self.tooltip_phase = 1
            self.prev_item = self.closest_item
            
        if self.tooltip_phase == 1:
            self.tooltip_time = min(self.tooltip_target, self.tooltip_time + self.tooltip_speed * dt)
            if self.tooltip_time >= self.tooltip_target:
                self.tooltip_phase = 2
        elif self.tooltip_phase == 2:
            self.tooltip_time = max(0, self.tooltip_time - self.tooltip_speed * dt)     
            if self.tooltip_time <= 0:
                self.tooltip_phase = 0   
        
        
        # item pickup
        if self.closest_item:
            if self.game.input.pressing('collect'):
                if self.closest_item.type == 'item' or self.closest_item.type.split('_')[0] == 'item':
                    player.pickup_item(self.closest_item)
            
                
                

    def render(self, surf, offset=(0, 0)):
        if self.closest_item:
            name = self.closest_item.item_data.info['name']
            
            x = self.closest_item.center[0] - offset[0]
            y = self.closest_item.center[1] - offset[1]
            
            
            
            points = [(x, y - 8), (x + 6, y - 14), (x + 6 + self.font.get_width(name) + 6 + self.tooltip_time, y - 14)]
            pygame.draw.lines(surf, (255, 255, 255), closed=False, points=points)
            self.font.render(surf, name, (x + 9, y - 23 - self.tooltip_time / 6))