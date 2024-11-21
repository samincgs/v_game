from .entity import Entity

class Enemy(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.player = self.game.world.player
        
    