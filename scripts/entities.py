from .player import Player
from .enemy import Bat
from .weapon import Weapon

class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        
        # default player items
        self.entities.append(Player(game, (200, 200), (9, 21), 'player'))
        self.entities[-1].inventory.add_item(Weapon(game, 'revolver', self.player, tags=['active']), 'weapons')
        
        self.entities.append(Bat(game, (100, 30), (15, 7)))
        
    @property
    def player(self):
        return self.entities[0]
       
    def update(self, dt):
        for entity in self.entities:
            kill = entity.update(dt)
            if kill:
                self.entities.remove(entity)

    def render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            entity.render(surf, offset=offset)
        
        