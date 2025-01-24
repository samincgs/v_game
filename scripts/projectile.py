import pygame
import math
import random

from scripts.spark import CurvedSpark
from scripts.effects import Goo
 
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
        
        for entity in self.game.world.entities.entities:
            if entity.type not in {'player', 'item'}:
                if (entity.rect.collidepoint(self.pos)) and (self.type not in  {'bat_goo'}):
                    entity.damage(self.config['power'])
                    angle = math.atan2(entity.pos[1] - self.game.world.entities.player.pos[1], entity.pos[0] - self.game.world.entities.player.pos[0])
                    entity.velocity[0] += math.cos(angle) * self.config['knockback'] * 150
                    entity.velocity[1] += math.sin(angle) * self.config['knockback'] * 150
                    for i in range(random.randint(8,12)):
                        self.game.world.spark_manager.sparks.append(CurvedSpark(pos=self.pos, speed=random.randint(30, 50) / 100 * 10 , curve=(random.random() * 0.5) - 0.1, angle=math.pi + angle + random.randint(-120, 120) / 100, decay_rate=random.randint(40, 70) / 100))
                    return True
        
        if any(collisions.values()):
            self.last_pos = self.pos.copy()
            if collisions['top']:
                angle = math.pi * 3 / 2
            if collisions['right']:
                angle = 0
            if collisions['bottom']:
                angle = math.pi / 2
            if collisions['left']:
                angle = math.pi
                
            # # add sparks
            if self.type in {'rifle', 'revolver', 'smg'}:
                for i in range(random.randint(2,4)):
                    self.game.world.spark_manager.sparks.append(CurvedSpark(pos=self.pos.copy(), speed=random.randint(30, 50) / 100 * 10 , curve=(random.random() * 0.1) - 0.05, angle=math.pi + angle + random.randint(-70, 70) / 100, decay_rate=random.randint(45, 75) / 100))
            elif self.type == 'bat_goo':
                self.game.world.projectile_manager.goo.append(Goo(self.game, self.game.assets.misc['goo'], self.last_pos, math.degrees(angle - math.pi / 2)))
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
        self.goo = []
    
    def add_projectile(self, game, pos, rot, speed, p_type):
        self.projectiles.append(Projectile(game, pos, rot, speed, p_type))
    
    def update(self, dt):
        for projectile in self.projectiles.copy():
            kill = projectile.update(dt)
            if kill:
                self.projectiles.remove(projectile)

        for goo in self.goo.copy():
            kill = goo.update(dt)
            if kill:
                self.goo.remove(goo)
                
    def render(self, surf, offset=(0, 0)):
        for projectile in self.projectiles:
            projectile.render(surf, offset=offset)
            
        for goo in self.goo:
            goo.render(surf, offset=offset)