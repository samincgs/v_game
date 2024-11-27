from .player import Player
from .weapon import Weapon

class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        
        # default player items
        self.entities.append(Player(game, (200, 200), (8, 17), 'player'))
        self.entities[-1].inventory.add_item(Weapon(game, 'golden_gun', self.entities[0], tags=['active']), 'weapons')
        
        
    def update(self, dt):
        for entity in self.entities:
            kill = entity.update(dt)
            if kill:
                self.entities.remove(entity)
            
    
    
    def render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            entity.render(surf, offset=offset)