import random

from .config import config
from .player import Player
from .enemy import ENEMIES
from .weapon import Weapon
from scripts.crate import Crate
from .itemdrop import Itemdrop
from .portal import Portal

class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        
        self.config = config['entities']
        
        
        
    @property
    def player(self):
        return self.entities[0]

    def drop_item(self, pos, size, item_data, velocity):
        self.entities.append(Itemdrop(self.game, pos, size, 'item', item_data))
        self.entities[-1].velocity = list(velocity)
    
    # additional
    def load_entities(self, tm):
        # player
        for entity in tm.extract(('spawner', (0, )), keep=False, offgrid=False):
            self.entities.append(Player(self.game, entity['pos'], self.config['player']['size'], 'player'))
            self.drop_item((260, 100), (1, 1), Weapon(self.game, 'revolver', None), [0, 160])
            self.player.inventory.add_item(Weapon(self.game, 'rifle', self.player, tags=['active']), 'weapons')
        
        # crates 
        for crate in tm.extract(('decor', (0, 1)), keep=False):
            self.entities.append(Crate(self.game, crate['pos'], [0, 0]))
            
        # portal
        for portal in tm.extract(('structures', (2,)), keep=False):
            self.entities.append(Portal(self.game, portal['pos'], [0, 0], 'portal'))
                
            
     
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
        
        