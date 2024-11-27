import pygame
import math
import random
 
from .config import config

class Projectile:
    def __init__(self, game, pos, rot, speed, p_type):
        self.game = game
        self.pos = list(pos)
        self.rot = rot
        self.speed = speed
        self.type = p_type
        self.config = config['projectiles'][p_type]
        self.timer = 0
        
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
        collisions = self.move(dt)
        self.timer += dt
        if any(collisions.values()):
            if collisions['top']:
                angle = math.pi * 3 / 2
            if collisions['right']:
                angle = 0
            if collisions['bottom']:
                angle = math.pi / 2
            if collisions['left']:
                angle = math.pi
            for i in range(random.randint(2,4)):
                self.game.world.spark_manager.add_spark('spark_curve', pos=self.pos, angle=math.pi + angle, speed= 4 + random.random() * 2, curve=-0.05 + random.random() * 0.1, color=(255, 255, 255), decay_rate=0.5 + random.random() * 0.2)
            return True

        if self.timer > 3:
            return True
        
        
        
    def render(self, surf, offset=(0, 0)):
        render_pos = [self.pos[0] - offset[0], self.pos[1] - offset[1]]
        p_len = self.config['shape'][2]
        if self.config['shape'][0] == 'line':
            pygame.draw.line(surf, self.config['shape'][1], render_pos, [render_pos[0] + math.cos(self.rot) * p_len, render_pos[1] + math.sin(self.rot) * p_len], self.config['shape'][3])

class ProjectileManager:
    def __init__(self):
        self.projectiles = []
    
    def add_projectile(self, game, pos, rot, speed, p_type):
        self.projectiles.append(Projectile(game, pos, rot, speed, p_type))
    
    def update(self, dt):
        for projectile in self.projectiles.copy():
            kill = projectile.update(dt)
            if kill:
                self.projectiles.remove(projectile)
                
    def render(self, surf, offset=(0, 0)):
        for projectile in self.projectiles:
            projectile.render(surf, offset=offset)