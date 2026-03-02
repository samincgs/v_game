import pygame

from .utils import palette_swap, glow_blit, outline
from .entities import Entity

class ParticleManager:
    def __init__(self):
        self.particles = []
    
    def reset(self):
        self.particles.clear()
    
    def update(self, dt):
        for particle in self.particles.copy():
            kill = particle.update(dt)
            if kill:
                self.particles.remove(particle)
                
    def render(self, surf, offset=(0, 0)):
        for particle in self.particles:
            particle.render(surf, offset=offset)

class Particle(Entity):
    def __init__(self, game, pos, velocity, p_type, decay_rate=0.1, start_frame=0, custom_color=None, custom_func=None, physics=None, damping=(0.8, -0.7), glow=None, glow_radius=None):
        super().__init__(game, pos, (1, 1), p_type)
        self.velocity = list(velocity)
        self.decay_rate = decay_rate
        self.frame = start_frame
        self.custom_color = custom_color
        self.custom_func = custom_func
        self.physics = physics
        self.damping = damping
        self.glow = glow # color
        self.glow_radius = glow_radius
        self.rotation = 0
        self.despawn = False
        self.set_action(p_type, force=True) 
        
        self.size = self.img.get_size()
        
    @property
    def img(self):
        if self.active_animation:
            img = self.active_animation.images[int(self.frame)]
            if self.active_animation.outline:
                self.outline = self.active_animation.outline
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.alpha:
            img.set_alpha(self.alpha)
        return img

    def set_action(self, action, force=False):
        if force or action != self.action:
            self.action = action
            self.active_animation = self.animations.new('particles' + '/' + (self.action or self.type))
    
    def update(self, dt):
        
        if not self.physics:
            self.pos[0] += self.velocity[0] * dt
            self.pos[1] += self.velocity[1] * dt
        else:
            self.pos[0] += self.velocity[0] * dt
            if self.physics and self.physics.tile_collide(self.pos):
                self.velocity[0] *= self.damping[1]
                self.velocity[1] *= self.damping[0]
            self.pos[1] += self.velocity[1] * dt
            if self.physics and self.physics.tile_collide(self.pos):
                self.velocity[0] *= self.damping[0]
                self.velocity[1] *= self.damping[1]
        if self.custom_func:
            self.custom_func(self, dt)
            
        self.frame += self.decay_rate * dt
        self.frame = min(self.frame, len(self.active_animation.images))
        if self.frame >= len(self.active_animation.images):
            self.despawn = True
                    
        return self.despawn
    
    def render(self, surf, offset=(0, 0)):
        img = self.img.copy()
        if self.custom_color:
            img = palette_swap(img, (255, 255, 255), self.custom_color)
            img.set_colorkey((0, 0, 0))
        if self.outline:
            outline(surf, img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2), self.outline)
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))
        if self.glow:
            glow_blit(surf, (self.pos[0] - offset[0] - self.glow_radius, self.pos[1] - offset[1] - self.glow_radius), self.glow_radius, self.glow)
        
        
            