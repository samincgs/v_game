import math

import scripts.pgtools as pt

from scripts.physics_entity import PhysicsEntity


class Itemdrop(PhysicsEntity):
    def __init__(self, game, pos, size, e_type, item_data):
        super().__init__(game, pos, size, e_type)
        self.item_data = item_data
        self.category = e_type
        self.type = e_type + '_' + item_data.name
        self.set_action('idle', force=True)
        
        self.size = (self.img.get_width(), self.img.get_height() - 2)
        
        self.timer = 0
    
       
    def update(self, dt):
        r = super().update(dt)
        return r
    
        
    def render(self, surf, offset=(0, 0)):
        if math.sin(self.pos[0] / 60 + self.game.world.master_clock * 4) > 0.5:
            color = (255, 255, 255, 255)
        else:
            color = (0, 0, 1, 100)        
        pt.utils.outline(surf, self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]), color=color)
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1])) 
        
        
    