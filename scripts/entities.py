import random

from .config import config
from .player import Player
from .enemy import ENEMIES
from .weapon import Weapon
from scripts.crate import Crate
from .itemdrop import Itemdrop

class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        
        self.config = config['entities']
        
        self.entities.append(Player(self.game, (240, 100), self.config['player']['size'], 'player'))
        
        
        # self.player.inventory.add_item(Weapon(game, 'rifle', self.player, tags=['active']), 'weapons')
        self.drop_item((260, 100), (1, 1), Weapon(self.game, 'revolver', None), [0, 160])
        
     
    @property
    def player(self):
        return self.entities[0]

    def drop_item(self, pos, size, item_data, velocity):
        self.entities.append(Itemdrop(self.game, pos, size, 'item', item_data))
        self.entities[-1].velocity = list(velocity)
    
    # additional
    def load_destructables(self, tm):
        for crate in tm.extract(['decor', (0, 1)], keep=False):
            self.entities.append(Crate(self.game, crate['pos'], [1, 1]))
     
    def spawner(self):
        if random.randint(1, self.config['bat']['spawn_rate']) == 1:
            
            spawn_point = (random.randint(-500, -200), random.randint(-100, 100))
            for i in range(3):
                self.entities.append(ENEMIES['bat'](self.game, spawn_point, self.config['bat']['size']))
    
    def update(self, dt):
        self.spawner()
                
        for entity in self.entities.copy():
            kill = entity.update(dt)
            if kill:
                self.entities.remove(entity)
    

    def render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            entity.render(surf, offset=offset)
        
        