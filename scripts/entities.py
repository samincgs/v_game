import random
import time

from scripts.config import config
from scripts.player import Player
from scripts.enemy import ENEMIES
from scripts.weapon import Weapon
from scripts.skill import DashSkill
from scripts.crate import Crate
from scripts.itemdrop import Itemdrop
from scripts.item import Item
from scripts.portal import Portal
from scripts.chicken import Chicken
from scripts.const import CRATE_RESPAWN_TIMER, TILE_RENDERS



class Entities:
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.items = []
        self.config = config['entities']
        
        self.crate_updates = {}
            
    @property
    def player(self):
        for entity in self.entities:
            if isinstance(entity, Player):
                return entity

    def drop_item(self, pos, size, item_data, velocity):
        self.items.append(Itemdrop(self.game, pos, size, 'item_drop', item_data))
        self.items[-1].velocity = list(velocity)
    
    def load_player(self, tm):
        player_extract = ('spawner', (0,))
        for entity in tm.extract(player_extract, keep=False, offgrid=True):
            self.entities.append(Player(self.game, entity['pos'], (9, 21), 'player'))
        
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
        
        self.player.inventory.add_item(DashSkill(self.game, self.player, 'dash', tags=['active']), 'skills')
    
    # additional
    def load_entities(self, tm):
        
            
        spawn_point = (random.randint(-500, -200), random.randint(-100, 100))
        for i in range(3):
            self.entities.append(ENEMIES['bat'](self.game, spawn_point, self.config['bat']['size']))
        
        # crates 
        crate_extract = ('decor', (0, 1))
        for crate in tm.extract(crate_extract, keep=False):
            crate = Crate(self.game, crate['pos'], [0, 0])
            self.entities.append(crate)
            self.crate_updates[crate.id] = {
                'current_time': time.time(),
                'trigger_time': -1,
                'pos': list(crate.pos)  
            }
            
        # portal
        portal_extract = ('structures', (2,))
        for portal in tm.extract(portal_extract, keep=False):
            self.entities.append(Portal(self.game, portal['pos'], [0, 0], 'portal'))
                
        # chicken   
        chicken_extract = ('spawner', (1,))
        for chicken in tm.extract(chicken_extract, keep=False, offgrid=False):
            self.entities.append(Chicken(self.game, chicken['pos'], [14, 14]))
            
        self.load_player(tm)
     
    def spawner(self):
        if random.randint(1, self.config['bat']['spawn_rate']) == 1:
            
            spawn_point = (random.randint(-500, -200), random.randint(-100, 100))
            for i in range(3):
                self.entities.append(ENEMIES['bat'](self.game, spawn_point, self.config['bat']['size']))
    
    def track_crate_updates(self):
        for crate_id in self.crate_updates:
            if self.crate_updates[crate_id]['trigger_time'] != -1:
                self.crate_updates[crate_id]['current_time'] = time.time()
                time_diff = self.crate_updates[crate_id]['current_time'] - self.crate_updates[crate_id]['trigger_time']
                if time_diff > CRATE_RESPAWN_TIMER: #TODO: add the fact that it can only spawn when not on screen
                    self.entities.append(Crate(self.game, self.crate_updates[crate_id]['pos'], [0, 0], cid=crate_id))
                    self.crate_updates[crate_id]['trigger_time'] = -1
    
    def update(self, dt):
        self.spawner()
        self.track_crate_updates()
        
        for item in self.items.copy():
            kill = item.update(dt)
            if kill:
                self.items.remove(item)
        
        for entity in self.entities.copy():
            kill = entity.update(dt)
            if kill:
                self.entities.remove(entity)


    def tile_render(self, surf, offset=(0, 0)):
        for entity in self.entities:
            if entity.type in TILE_RENDERS: 
                entity.render(surf, offset=offset)
    
    def render(self, surf, offset=(0, 0)):
        
        for item in self.items:
            item.render(surf, offset=offset)
        
        for entity in self.entities:
            if entity.type not in TILE_RENDERS:
                entity.render(surf, offset=offset)
        
        