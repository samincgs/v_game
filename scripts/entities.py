import random

from .config import config
from .player import Player
from .enemy import Bat
from .weapon import Weapon
from .item import Item
from .itemdrop import Itemdrop

class Entities:
    def __init__(self, game):
        self.game = game
        self.config = config['entities']
        
        self.entities = []
        
        # default player items
        self.entities.append(Player(game, (200, 120), self.config['player']['size'], 'player'))
        self.player.inventory.add_item(Weapon(game, 'revolver', self.player, tags=['active']), 'weapons')
        self.player.inventory.add_item(Weapon(game, 'rifle', self.player, tags=['active']), 'weapons')
        self.player.inventory.add_item(Weapon(game, 'smg', self.player), 'weapons')
        self.player.inventory.add_item(Item(game, 'bat_wing', self.player, 3), 'items')
        self.player.inventory.add_item(Item(game, 'wood', self.player, 7), 'items')
        
    @property
    def player(self):
        return self.entities[0]

    def drop_item(self, pos, size,item_data ,velocity):
        self.entities.append(Itemdrop(self.game, pos, size, 'item', item_data, velocity))
    
    def spawner(self):
        if random.randint(1, self.config['bat']['spawn_rate']) == 1:
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
        
        