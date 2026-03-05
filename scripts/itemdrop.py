import math

import scripts.pgtools as pt

from scripts.physics_entity import PhysicsEntity
from scripts.config import config


class Itemdrop(PhysicsEntity):
    def __init__(self, game, pos, size, e_type, item_data):
        super().__init__(game, pos, size, e_type)
        self.item_data = item_data
        self.type = 'item' + '_' + item_data.name
        self.set_action('idle', force=True)
        self.category = config['items'][item_data.name]['name'] if item_data.name in config['items'] else str(item_data.name).title()
        self.size = (self.img.get_width(), self.img.get_height() - 2)
        
        self.grass_effect = (3, 6)
        
        self.timer = 0
    
       
    def update(self, dt):
        r = super().update(dt)
        
        force_point = (self.rect.centerx, self.rect.bottom)
        self.game.world.grass_manager.apply_bend(force_point, self.grass_effect[0], self.grass_effect[1])   
        
        return r
    
        
    def render(self, surf, offset=(0, 0)):
        color = (0, 0, 1, 100)        
        
        if not self.game.window.pause_state:
            if math.sin(self.pos[0] / 60 + self.game.world.master_clock * 4) > 0.5:
                color = (255, 255, 255, 255)
        pt.utils.outline(surf, self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1] - 2), color=color)
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1] - 2)) 
        
        
    