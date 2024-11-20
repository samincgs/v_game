import pygame

from .entity import Entity

class Enemy(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.player = self.game.world.player
        
    def get_angle(self, target):
        pass
    
    def get_distance(self, target):
        pass
    
    def in_range(self, target, radius):
        return self.get_distance(target) <= radius
    
    def update(self, dt):
        pass