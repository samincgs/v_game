import pygame
import math
import time

from .config import config
from .projectile import Projectile

class Weapon:
    def __init__(self, game, owner, w_type):
        self.game = game
        self.owner = owner
        self.type = w_type
        self.config = config['weapons']
        self.projectile_type = self.config[self.type]['projectile_type']
        self.capacity = self.config[self.type]['capacity']
        self.ammo = self.capacity
        self.attack_rate = self.config[self.type]['attack_rate']
        self.trigger = self.config[self.type]['trigger']
        
        self.rotation = 0
        self.flip = False
        self.last_attack = 0
    
    def attack(self):
        if (self.ammo > 0):
            self.ammo -= 1
            curr_time = time.time()
            if curr_time - self.last_attack >= self.attack_rate:
                self.game.world.player.projectiles.append(Projectile(self.game, self.owner.center, math.radians(self.rotation), 300, self.type))
                self.last_attack = curr_time
    
    def reload(self):
        self.ammo = self.capacity
       
    def render(self, surf, loc):
        img = self.game.assets.weapons[self.type].copy()
        if (self.rotation % 360 > 90) and (self.rotation % 360 < 270):
            img = pygame.transform.flip(img, False, True)
            self.flip = True
        else:
            self.flip = False
        img = pygame.transform.rotate(img, -self.rotation)
        surf.blit(img, (loc[0] - img.get_width() // 2, loc[1] - img.get_height() // 2))
            
        