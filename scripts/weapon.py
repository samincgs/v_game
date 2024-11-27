import pygame
import math
import time
import random

from .item import Item
from .config import config

class Weapon(Item):
    def __init__(self, game, name, owner, tags=None):
        weapon_tags = ['weapon']
        if tags:
            weapon_tags.extend(tags)
        
        super().__init__(game, name, owner=owner, tags=weapon_tags)
        self.config = config['weapons'][self.name]
        self.projectile_type = self.config['projectile_type']
        self.max_ammo = self.config['max_ammo']
        self.capacity = self.config['capacity']
        self.ammo = self.capacity
        self.reload_method = self.config['reload_method']
        self.attack_rate = self.config['attack_rate']
        self.trigger = self.config['trigger']
        
        self.rotation = 0
        self.flip = False
        self.last_attack = 0
    
    @property
    def img(self):
        img = self.game.assets.weapons[self.name].copy()
        return img
    
    def attack(self):
        if (self.ammo > 0):
            curr_time = time.time()
            if curr_time - self.last_attack >= self.attack_rate:
                self.ammo -= 1
                self.game.world.projectile_manager.add_projectile(self.game, self.owner.center, math.radians(self.rotation), 300, self.name)
                self.last_attack = curr_time
                # add bow sparks
                spark_position = [
                self.owner.center[0] + math.cos(math.radians(self.rotation)) * 4,
                self.owner.center[1] + math.sin(math.radians(self.rotation)) * 4
            ]
                self.game.world.vfx.spawn_group('bow_sparks', spark_position, math.radians(self.rotation))
                
                if self.name in ['rifle', 'smg']:
                    if self.ammo %  2 == 0:
                        self.game.world.particle_manager.add_particle(self.game, 'shells', self.owner.center, movement=[(self.owner.flip[0] - 0.5) * random.randint(60, 90), -random.randint(30, 50)], decay_rate=0.05, frame=0, custom_color=(244, 176, 60), physics=self.game.world.tilemap)
    
    def reload(self):
        if (self.ammo != self.capacity) and (self.max_ammo > 0):
            diff = min(self.max_ammo, self.capacity - self.ammo) # use min so when player has almost no ammunication left, the game doesnt crash 
            self.max_ammo -= diff
            self.ammo = self.capacity
            
            if self.reload_method == 'shells':
                for i in range(diff):
                    self.game.world.particle_manager.add_particle(game=self.game, 
                        p_type='shells', 
                        pos=self.owner.center, 
                        movement=[(self.owner.flip[0] - 0.5) * random.randint(60, 90), -random.randint(40, 80)], 
                        decay_rate=0.1, 
                        frame=0, 
                        custom_color=(244, 176, 60),  # (maybe) change the color of the reload bullet drop
                        physics=self.game.world.tilemap)
            elif self.reload_method == 'mag':
                self.game.world.particle_manager.add_particle(game=self.game, 
                        p_type='mag', 
                        pos=self.owner.center, 
                        movement=[(self.owner.flip[0] - 0.5) * random.randint(40, 70), -random.randint(30, 60)], 
                        decay_rate=0.1, 
                        frame=0, 
                        custom_color=(92, 36, 27),
                        physics=self.game.world.tilemap)
        

    def render(self, surf, loc):
        img = self.img
        if (self.rotation % 360 > 90) and (self.rotation % 360 < 270):
            img = pygame.transform.flip(img, False, True)
            self.flip = True
        else:
            self.flip = False
        img = pygame.transform.rotate(img, -self.rotation)
        surf.blit(img, (loc[0] - img.get_width() // 2, loc[1] - img.get_height() // 2))
            
        