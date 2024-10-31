import pygame
import math

from .config import config
from .projectile import Projectile

class Weapon:
    def __init__(self, game, owner, w_type):
        self.game = game
        self.owner = owner
        self.type = w_type
        self.projectile_type = config['weapons'][self.type]['projectile_type']
        self.capacity = config['weapons'][self.type]['capacity']
        self.ammo = self.capacity
        self.attack_rate = config['weapons'][self.type]['attack_rate']
        self.trigger = config['weapons'][self.type]['trigger']
        
        self.rotation = 0
        self.flip = False
    
    def attack(self):
        # if (self.ammo > 0):
        #     self.ammo -= 1
        self.game.world.player.projectiles.append(Projectile(self.game, self.owner.center, math.radians(self.rotation), 300, self.type))
        
    def render(self, surf, loc):
        img = self.game.assets.weapons[self.type].copy()
        if (self.rotation % 360 > 90) and (self.rotation % 360 < 270):
            img = pygame.transform.flip(img, False, True)
            self.flip = True
        else:
            self.flip = False
        img = pygame.transform.rotate(img, -self.rotation)
        surf.blit(img, (loc[0] - img.get_width() // 2, loc[1] - img.get_height() // 2))
            
        