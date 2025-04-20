
from .entity import Entity
from .config import config

class Portal(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        
        self.size = (self.img.get_width(), self.img.get_height())
        self.config = config['portals']
        
        
    def update(self, dt):
        
        r = super().update(dt)
        
        if r:
            return r
        
        current_map_area = self.game.world.map_area
        if self.game.world.player.rect.colliderect(self.rect) and self.game.world.transition == 0:
            if current_map_area in self.config:
                self.game.world.start_transition(self.config[current_map_area]['target'])