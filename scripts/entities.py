import random

from scripts.config import config
from scripts.player import Player
from scripts.enemy import ENEMIES
from scripts.weapon import Weapon
from scripts.crate import Crate
from scripts.itemdrop import Itemdrop
from scripts.item import Item
from scripts.portal import Portal

class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        
        self.config = config['entities']
        
        self.tile_renders = ['crate', 'portal']
    
    @property
    def player(self):
        return self.entities[0] if len(self.entities) else None

    def drop_item(self, pos, size, item_data, velocity):
        self.entities.append(Itemdrop(self.game, pos, size, 'item', item_data))
        self.entities[-1].velocity = list(velocity)
    
    # additional
    def load_entities(self, tm):
        # player
        player_extract = ('spawner', (0,))
        for entity in tm.extract(player_extract, keep=False, offgrid=False):
            self.entities.append(Player(self.game, entity['pos'], (10, 21), 'player'))
            self.player.inventory.add_item(Weapon(self.game, 'revolver', self.player, tags=['active']), 'weapons')
            self.player.inventory.add_item(Weapon(self.game, 'old_knife', self.player, tags=['active']), 'weapons')
            self.drop_item((entity['pos'][0] + 20, entity['pos'][1]), (0, 0), Weapon(self.game, 'rifle', None), [0, -3])
            
            self.player.inventory.add_item(Item(self.game, 'wood', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'wood', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'wood', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'iron', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'iron', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'apple', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'apple', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'apple', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'apple', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'bat_wing', self.player), 'items')
            self.player.inventory.add_item(Item(self.game, 'bat_wing', self.player), 'items')
            
            # spawn_point = (random.randint(-500, -200), random.randint(-100, 100))
            # for i in range(3):
            #     self.entities.append(ENEMIES['bat'](self.game, spawn_point, self.config['bat']['size']))
        
        # crates 
        crate_extract = ('decor', (0, 1))
        for crate in tm.extract(crate_extract, keep=False):
            self.entities.append(Crate(self.game, crate['pos'], [0, 0]))
            
        # portal
        portal_extract = ('structures', (2,))
        for portal in tm.extract(portal_extract, keep=False):
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
    

    def tile_render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            if entity.type in self.tile_renders: 
                entity.render(surf, offset=offset)
    
    def render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            if entity.type not in self.tile_renders:
                entity.render(surf, offset=offset)
        
        