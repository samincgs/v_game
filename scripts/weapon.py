import pygame
import math
import time
import random

from .config import config
from .projectile import Projectile

class Weapon:
    def __init__(self, game, owner, w_type):
        self.game = game
        self.owner = owner
        self.type = w_type
        self.config = config['weapons'][self.type]
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
    
    def attack(self):
        if (self.ammo > 0):
            curr_time = time.time()
            if curr_time - self.last_attack >= self.attack_rate:
                self.ammo -= 1
                self.game.world.player.projectiles.append(Projectile(self.game, self.owner.center, math.radians(self.rotation), 300, self.type))
                self.last_attack = curr_time
    
    def reload(self):
        if (self.ammo != self.capacity) and (self.max_ammo > 0):
            self.max_ammo -= self.capacity - self.ammo
            self.ammo = self.capacity
            
            if self.reload_method == 'shells':
                for i in range(1):
                    self.game.world.particle_manager.add_particle(game=self.game, 
                        p_type='shells', 
                        pos=self.owner.center, 
                        movement=[(self.owner.flip[0] - 0.5) * random.randint(60, 90), -random.randint(40, 80)], 
                        decay_rate=0.1, 
                        frame=0, 
                        custom_color=(244, 176, 60), 
                        physics=self.game.world.tilemap)
        
       
    def render(self, surf, loc):
        img = self.game.assets.weapons[self.type].copy()
        if (self.rotation % 360 > 90) and (self.rotation % 360 < 270):
            img = pygame.transform.flip(img, False, True)
            self.flip = True
        else:
            self.flip = False
        img = pygame.transform.rotate(img, -self.rotation)
        surf.blit(img, (loc[0] - img.get_width() // 2, loc[1] - img.get_height() // 2))
            
        