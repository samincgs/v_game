import math

from scripts.item import Item

from .entity import Entity
from .utils import normalize, outline

class Itemdrop(Entity):
    def __init__(self, game, pos, size, e_type, item_data, velocity):
        super().__init__(game, pos, size, e_type)
        self.item_data = item_data
        self.velocity = list(velocity)
        
        
        self.set_action(self.item_data.name)
        self.size = (self.img.get_width(), self.img.get_height() - 1)
        
        
    def update(self, dt):
        super().update(dt)
        
        self.velocity[0] = normalize(self.velocity[0], 350 * dt)
        self.velocity[1] = normalize(self.velocity[1], 350 * dt)
        
        self.motion = self.velocity.copy()
        
        self.motion[0] *= dt
        self.motion[1] *= dt
                      
        last_collisions = self.collisions(self.game.world.tilemap, movement=self.motion)
        
        if last_collisions['bottom']:
            self.velocity[1] = 0
          
        self.velocity[1] = min(500, self.velocity[1] + dt * 700)
        
        # pick up on collision
        player = self.game.world.player
            
        if self.type == 'item' and player.rect.colliderect(self.rect):
            player.inventory.add_item(Item(self.game, self.item_data.name, player), str(self.type + 's'))
            return True
        
    
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
    