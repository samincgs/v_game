import pygame
import math
import random

from .const import ENTITY_COLLIDEABLES

class SwordArc:
    def __init__(self, game, owner, pos, radius, speed, shift, angle, duration=2, decay_rate=0):
        self.game = game
        self.owner = owner
        self.pos = list(pos)
        self.radius = radius
        self.speed = speed
        self.shift = shift
        self.angle = angle
        self.life_time = 0
        self.duration = duration
        self.decay_rate = decay_rate
        self.collided = False
        self.knockback = 1
        self.damage = 10
        
        self.sword_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.arc_color = (255, 80, 80)
        self.sword_mask = None
        
    def update(self, dt):
        # move slightly in direction
        self.pos[0] += math.cos(math.radians(self.angle + 180)) * self.speed * dt
        self.pos[1] += math.sin(math.radians(self.angle + 180)) * self.speed * dt
        
        hit = False
        for entity in self.game.world.entities.entities:
            if entity.type not in ENTITY_COLLIDEABLES:
                if entity.type != self.owner.type:
                    self.sword_mask = pygame.mask.from_surface(self.sword_surf)
                    entity_mask = pygame.mask.from_surface(entity.img)
                    if self.sword_mask.overlap(entity_mask, (int(self.pos[0] - entity.pos[0]), int(self.pos[1] - entity.pos[1]))) and not self.collided:
                        hit = True
                        entity.damage(self.damage)
                        angle = math.atan2(entity.pos[1] - self.game.world.entities.player.pos[1], entity.pos[0] - self.game.world.entities.player.pos[0])
                        entity.velocity[0] += math.cos(angle) * self.knockback * 150
                        entity.velocity[1] += math.sin(angle) * self.knockback * 150
        
        if hit:
            self.collided = True
        
        self.life_time = min(self.life_time + self.decay_rate * dt, self.duration)
        if self.life_time >= self.duration:
            return True
    
    def render(self, surf, offset=(0, 0)):
        self.sword_surf.fill((0, 0, 0, 0))

        pygame.draw.circle(self.sword_surf, self.arc_color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(
            self.sword_surf,
            (0, 0, 0, 0), 
            (self.radius + self.shift[0], self.radius),
            self.radius
        )
        rotated_surf = pygame.transform.rotate(self.sword_surf, -self.angle)
        rect = rotated_surf.get_rect(center=(self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(rotated_surf, rect)
