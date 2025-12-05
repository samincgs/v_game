import random

from scripts.physics_entity import PhysicsEntity 
from scripts.item import create_item

class Crate(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'crate')
        self.velocity_normalization = [200, 0]
        
        
        self.size = (self.img.get_width(), self.img.get_height())
        
        self.drops = [create_item(game, random.choice(['wood', 'wood', 'iron', 'apple']), None) for i in range(random.randint(0, 2))]
        