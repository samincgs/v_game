import math

from .physics_entity import PhysicsEntity
from .utils import outline

class Itemdrop(PhysicsEntity):
    def __init__(self, game, pos, size, e_type, item_data):
        super().__init__(game, pos, size, e_type)
        self.item_data = item_data
        
        self.set_action(self.item_data.name)
        
        self.size = (self.img.get_width(), self.img.get_height())
        
        
    def render(self, surf, offset=(0, 0)):
        if math.sin(self.game.world.master_clock * 4) > 0.5:
            color = (255, 255, 255, 255)
        else:
            color = (0, 0, 1, 100)
        
        # item_render_offset = (-10, -30)
        # if self.get_distance(self.game.world.player) < 10:
        #     self.game.assets.fonts['small_white'].render(surf, str(self.item_data.name), (self.pos[0] - offset[0] + item_render_offset[0], self.pos[1] - offset[1] + item_render_offset[1]))
        
        outline(surf, self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]), color=color)
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1])) 
    