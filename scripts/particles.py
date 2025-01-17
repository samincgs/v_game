import pygame
import math

from .utils import palette_swap

class Particle:
    def __init__(self, game, p_type, pos, movement, decay_rate=0.1, frame=0, custom_color=None, physics=None):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.movement = list(movement)
        self.decay_rate = decay_rate
        self.frame = frame
        self.color = custom_color
        self.physics = physics
        self.spawn = True
        self.rotation = 0
        
    def update(self, dt):
        
        if self.type in ['shells', 'mag']:
            self.movement[1] += 300 * dt
            abs_motion = abs(self.movement[1]) + abs(self.movement[0])
            if abs_motion > 12:
                self.rotation += 20 * dt * abs_motion
  
        if not self.physics:
            self.pos[0] += self.movement[0] * dt
            self.pos[1] += self.movement[1] * dt
        else:
            # horizontal collision
            hit = False
            self.pos[0] += self.movement[0] * dt
            if self.physics.tile_collide(self.pos):
                self.movement[0] *= -0.7
                self.movement[1] *= 0.8
                hit = True
            # vertical collision
            self.pos[1] += self.movement[1] * dt
            if self.physics.tile_collide(self.pos):
                self.movement[0] *= 0.8
                self.movement[1] *= -0.7
                hit = True
            if hit:
                self.pos[0] += self.movement[0] * dt * 3
                self.pos[1] += self.movement[1] * dt * 3
        
        self.frame += self.decay_rate * dt
        self.frame = min(self.frame, len(self.game.assets.particles[self.type]) - 1)
        if self.frame >= len(self.game.assets.particles[self.type]) - 1:
            self.spawn = False
                                                                                                    
        return not self.spawn
    
    def render(self, surf, offset=(0,0)):
        img = self.game.assets.particles[self.type][int(self.frame)]
        if self.color:
            img = palette_swap(img, (255, 255, 255), self.color)
            img.set_colorkey((0, 0, 0))
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.spawn:
            surf.blit(img, (self.pos[0] - img.get_width() // 2 - offset[0], self.pos[1] - img.get_height() // 2 - offset[1] + 1))
        

class DestructionParticle:
    def __init__(self, game, img, pos, rot, rot_speed, velocity, duration=3, physics=None):
        self.game = game
        self.img = img
        self.pos = list(pos)
        self.rotation = rot
        self.rotation_speed = rot_speed
        self.velocity = list(velocity)
        self.physics = physics
        self.rotation = 0
        self.duration = duration
        
    def update(self, dt):
        
        self.duration -= dt
        
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        self.velocity[1] += 200 * dt
        self.rotation += self.rotation_speed * dt
    
        if self.duration <= 0:
            return not self.duration

    
    def render(self, surf, offset=(0, 0)):
        if self.rotation:
            self.img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(self.img, (self.pos[0] - self.img.get_width() // 2 - offset[0], self.pos[1] - self.img.get_height() // 2 - offset[1]))
             
class ParticleManager:
    def __init__(self):
        self.particles = []
        self.destruction_particles = []
    
    def add_particle(self, game, p_type, pos, movement, decay_rate=0.1, frame=0, custom_color=None, physics=None):
        self.particles.append(Particle(game, p_type, pos, movement, decay_rate, frame, custom_color, physics))
    
    def add_death_particle(self, game, img, pos, rot, rot_speed, velocity, duration=3, physics=None):
        self.destruction_particles.append(DestructionParticle(game, img, pos, rot, rot_speed, velocity, duration, physics))
    
    def update(self, dt):
        for particle in self.destruction_particles.copy():
            kill = particle.update(dt)
            if kill:
                self.destruction_particles.remove(particle)
                
        for particle in self.particles.copy():
            kill = particle.update(dt)
            if kill:
                self.particles.remove(particle)

    def render(self, surf, offset=(0, 0)):
        for particle in self.destruction_particles:
            particle.render(surf, offset=offset)
    
        for particle in self.particles:
            particle.render(surf, offset=offset)
            
     
                       