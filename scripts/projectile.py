import pygame
import math

from .config import config

class Projectile:
    def __init__(self, game, pos, rot, speed, p_type):
        self.game = game
        self.pos = list(pos)
        self.rot = rot
        self.speed = speed
        self.type = p_type
        self.config = config['projectiles'][p_type]
        
    def move(self, dt):
        directions = {d: False for d in ['top', 'left', 'bottom', 'right']}
        
        dx = math.cos(self.rot) * self.speed * dt
        self.pos[0] += dx
        
        if self.game.world.tilemap.tile_collide(self.pos):
            if dx > 0:
                directions['right'] = True
            else:
                directions['left'] = True 
            return directions
                
        dy = math.sin(self.rot) * self.speed * dt
        self.pos[1] += dy
        
        if self.game.world.tilemap.tile_collide(self.pos):
            if dy > 0:
                directions['bottom'] = True
            else:
                directions['top'] = True
            return directions
        
        return directions
                
                
    def update(self, dt):
        directions = self.move(dt)
        return any(directions.values())
        
        
    def render(self, surf, offset=(0, 0)):
        render_pos = [self.pos[0] - offset[0], self.pos[1] - offset[1]]
        p_len = self.config['shape'][2]
        if self.config['shape'][0] == 'line':
            pygame.draw.line(surf, self.config['shape'][1], render_pos, [render_pos[0] + math.cos(self.rot) * p_len, render_pos[1] + math.sin(self.rot) * p_len], self.config['shape'][3])