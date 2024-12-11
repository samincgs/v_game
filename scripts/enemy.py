import math
import random

from .entity import Entity
from .utils import normalize

class Bat(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'bat')
        self.velocity = [0, 0]
        self.attack_timer = 0
        
    def update(self, dt):
        super().update(dt)
        self.attack_timer += dt
        
        self.velocity[0] = normalize(self.velocity[0], 350 * dt)
        self.velocity[1] = normalize(self.velocity[1], 350 * dt)
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        
        
        
        
        
        
        