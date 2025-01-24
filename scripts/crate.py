import random

from .physics_entity import PhysicsEntity
from .item import create_item


class Crate(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'crate')
        self.velocity_normalization = [200, 0]
        
        if self.type + '_idle' in self.game.assets.animations.animations:
            self.set_action('idle')
        
        self.size = (self.img.get_width(), self.img.get_height())
        
        self.drops = [create_item(game, random.choice(['wood', 'wood', 'iron']), self) for i in range(random.randint(0, 2))]
        