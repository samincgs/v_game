from .physics_entity import PhysicsEntity


class Crate(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'crate')
        self.velocity_normalization = [5, 0]
        
        if self.type + '_idle' in self.game.assets.animations.animations:
            self.set_action('idle')
        
        self.size = (self.img.get_width(), self.img.get_height() - 2)
        