import random

from .config import config
from .player import Player
from .enemy import Bat
from .weapon import Weapon

class Entities:
    def __init__(self, game):
        self.game = game
        self.config = config['entities']
        
        self.entities = []
        
        # default player items
        self.entities.append(Player(game, (200, 120), self.config['player']['size'], 'player'))
        self.entities[-1].inventory.add_item(Weapon(game, 'revolver', self.player, tags=['active']), 'weapons')
        
        
        
    @property
    def player(self):
        return self.entities[0]
    
    
    def spawner(self):
        if random.randint(1, self.config['bat']['spawn_rate']) == 1:
            print('pog')
            spawn_point = (random.randint(-500, -200), random.randint(-100, 100))
            for i in range(3):
                self.entities.append(Bat(self.game, spawn_point, self.config['bat']['size']))
    
    def update(self, dt):
        self.spawner()
        
        for entity in self.entities.copy():
            kill = entity.update(dt)
            if kill:
                self.entities.remove(entity)

    def render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            entity.render(surf, offset=offset)
        
        