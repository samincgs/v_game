from .entity import Entity
from .utils import normalize

class Itemdrop(Entity):
    def __init__(self, game, pos, size, e_type, item_data, velocity):
        super().__init__(game, pos, size, e_type)
        self.item_data = item_data
        self.velocity = list(velocity)
        self.size = (self.img.get_width(), self.img.get_height() - 1)
        
        self.set_action(self.item_data.name)
        
    def update(self, dt):
        super().update(dt)
        
        self.velocity[1] = normalize(self.velocity[1], 250 * dt)
        
        self.motion = self.velocity.copy()
        
        last_collisions = self.collisions(self.game.world.tilemap, movement=self.motion)
        
        if last_collisions['bottom']:
            self.velocity[1] = 0
        
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
    