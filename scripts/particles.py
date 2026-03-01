import pygame
import math
import random

import scripts.pgtools as pt

from scripts.pgtools.utils import glow_blit

class ParticleManager(pt.ParticleManager):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.grass_particles = []
        self.destruction_particles = []

    def add_particle(self, *args, **kwargs):
        self.particles.append(Particle(*args, **kwargs))
        
    def add_death_particle(self, *args, **kwargs):
        self.destruction_particles.append(DestructionParticle(*args, **kwargs))
    
    def environment_particles(self, surf):
        # leaf particles
        leaf_extract = ('foliage', (0, 1))
        for tree in self.game.world.tilemap.extract(leaf_extract, keep=True):
            # if the tree is visible on the players screen
            if (self.game.world.camera.pos[0] <=  tree['pos'][0] + self.game.world.tilemap.tiles['foliage'][1].get_width() <= (self.game.world.camera.pos[0] + surf.get_width())) or (self.game.world.camera.pos[0] <=  tree['pos'][0] <= (self.game.world.camera.pos[0] + surf.get_width())):
                r = pygame.Rect(tree['pos'][0] + 9, tree['pos'][1] + 8, 44, 17)
                if random.randint(0, 1200) < (r.width - r.height):
                    pos = [r.x + random.random() * r.width, r.y + random.random() * r.height]
                    color = (random.randint(100, 150), random.randint(80, 130), random.randint(10, 50))
                    self.particles.append(Particle(self.game, pos, [random.randint(-60, -35), random.randint(35, 50)], 'leaf', start_frame=random.randint(0, 1), custom_color=color, decay_rate=1.4))
            
        # grass particles    
        
        
        
        
               
    def update(self, dt):
        for particle in self.destruction_particles.copy():
            kill = particle.update(dt)
            if kill:
                self.destruction_particles.remove(particle)
        super().update(dt)

    def render(self, surf, offset=(0, 0)):
        for particle in self.destruction_particles:
            particle.render(surf, offset=offset)
    
        for particle in self.particles:
            particle.render(surf, offset=offset)
            
        self.environment_particles(surf)

class Particle(pt.Particle):
    def __init__(self, game, pos, velocity, p_type, decay_rate=0.1, start_frame=0, custom_color=None, custom_func=None, physics=None, damping=(0.8, -0.7), glow=None, glow_radius=None):
        super().__init__(game, pos, velocity, p_type, decay_rate, start_frame, custom_color, custom_func, physics, damping, glow, glow_radius)
        self.spawn = True
        self.wind_force = 0
        
    def update(self, dt):
        if self.type in ['shells', 'mag']:
            self.velocity[1] += 300 * dt
            abs_motion = abs(self.velocity[1]) + abs(self.velocity[0])
            if abs_motion > 20:
                self.rotation += 20 * dt * abs_motion
        elif self.type == 'leaf':
            # TODO: fix sin wave
            self.pos[0] += math.sin(self.frame * 0.76) * 0.21
            # if not self.wind_force:
            #     if random.randint(0, 999) == 1:
            #         self.wind_force = 0.6
            # else:
            #     self.pos[0] -= self.wind_force * dt
            
        if not self.physics:
            self.pos[0] += self.velocity[0] * dt
            self.pos[1] += self.velocity[1] * dt
        else:
            # horizontal collision
            hit = False
            self.pos[0] += self.velocity[0] * dt
            if self.physics.tile_collide(self.pos):
                self.velocity[0] *= -0.7
                self.velocity[1] *= 0.8
                hit = True
            # vertical collision
            self.pos[1] += self.velocity[1] * dt
            if self.physics.tile_collide(self.pos):
                self.velocity[0] *= 0.8
                self.velocity[1] *= -0.7
                hit = True
            if hit:
                self.pos[0] += self.velocity[0] * dt * 2
                self.pos[1] += self.velocity[1] * dt * 2
        
        self.frame += self.decay_rate * dt
        self.frame = min(self.frame, len(self.active_animation.images))
        if self.frame >= len(self.active_animation.images):
            self.despawn = True
                    
        return self.despawn
    
    def render(self, surf, offset=(0,0)):
        img = self.img
        if self.custom_color:
            img = pt.utils.palette_swap(img, (255, 255, 255), self.custom_color)
            img.set_colorkey((0, 0, 0))
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        surf.blit(img, (self.pos[0] - img.get_width() // 2 - offset[0], self.pos[1] - img.get_height() // 2 - offset[1] + 1))
        if self.glow:
            glow_blit(surf, (self.pos[0] - offset[0] - self.glow_radius, self.pos[1] - offset[1] - self.glow_radius), self.glow_radius, self.glow)
        

class DestructionParticle:
    def __init__(self, game, img, pos, rot, rot_speed, decay_rate, velocity, duration=3, physics=None):
        self.game = game
        self.img = img
        self.pos = list(pos)
        self.rotation = rot
        self.rotation_speed = rot_speed
        self.velocity = list(velocity)
        self.physics = physics
        self.rotation = 0
        self.duration = duration
        self.decay_rate = decay_rate
        
    def update(self, dt):
        
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        
        self.velocity[1] = min(300, self.velocity[1] + dt * 500)
        
        self.rotation += self.rotation_speed * dt 

        self.duration -= max(self.decay_rate * dt, 0)
        if self.duration <= 0:
            return self.duration

    
    def render(self, surf, offset=(0, 0)):
        img = self.img.copy()
        if self.rotation:
            img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(img, (self.pos[0] - self.img.get_width() // 2 - offset[0], self.pos[1] - self.img.get_height() // 2 - offset[1]))
             

            
     
                       