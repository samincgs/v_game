import random
import time

from scripts.physics_entity import PhysicsEntity 
from scripts.item import create_item

class Crate(PhysicsEntity):
    def __init__(self, game, pos, size, cid=None):
        super().__init__(game, pos, size, 'crate')
        self.velocity_normalization = [200, 0]
        self.size = (self.img.get_width(), self.img.get_height())
        self.drops = [create_item(game, random.choice(['wood', 'wood', 'iron', 'apple']), owner=None) for i in range(random.randint(0, 2))]
        self.grass_effect = (8, 16)
        self.id = random.randint(1, 2**31 - 1) if not cid else cid

            
    def update(self, dt):
        r = super().update(dt)

        force_point = (self.rect.centerx, self.rect.bottom)
        self.game.world.grass_manager.apply_bend(force_point, self.grass_effect[0], self.grass_effect[1])    
        
        if r:
            self.game.world.entities.crate_updates[self.id]['trigger_time'] = time.time()
                
        return r