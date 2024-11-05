import pygame

from .utils import palette_swap

class Particle:
    def __init__(self, game, p_type, pos, movement, decay_rate, frame=0, custom_color=None, physics=None):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.movement = list(movement)
        self.decay_rate = decay_rate
        self.frame = frame
        self.color = custom_color
        self.physics = physics
        
        self.lifespan = len(self.game.assets.particles[self.type]) + 1 - frame
        self.spawn = True
        self.rotation = 0
        
    def update(self, dt):
        
        self.pos[0] += self.movement[0] * dt
        self.pos[1] += self.movement[1] * dt
        
        self.frame += self.decay_rate * dt
        
        self.rotation += 200 * dt  
        
        if self.type in ['shells']:
            self.movement[1] += 300 * dt
        
        if self.physics:
            if self.physics.tile_collide(self.pos):
                pass
        
        self.lifespan -= dt
        if self.lifespan <= 0:
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
            surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            
            
class ParticleManager:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, game, p_type, pos, movement, decay_rate, frame=0, custom_color=None, physics=None):
        self.particles.append(Particle(game, p_type, pos, movement, decay_rate, frame, custom_color, physics))
    
    def update(self, dt):
        for particle in self.particles.copy():
            kill = particle.update(dt)
            if kill:
                self.particles.remove(particle)
                
    def render(self, surf, offset=(0, 0)):
        for particle in self.particles:
            particle.render(surf, offset=offset)
    
                       