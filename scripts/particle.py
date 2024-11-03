import pygame


class Particle:
    def __init__(self, game, p_type, pos, movement, decay_rate, frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.movement = list(movement)
        self.decay_rate = decay_rate
        self.frame = frame
        self.lifespan = len(self.game.assets.particles[self.type]) + 1 - frame
        self.spawn = True 
        
    def update(self, dt):
        
        self.pos[0] += self.movement[0] * dt
        self.pos[1] += self.movement[1] * dt
        
        self.frame += self.decay_rate * dt
        
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.spawn = False
        
        return self.spawn
    
    
    def render(self, surf, offset=(0,0)):
        img = self.game.assets.particles[self.type][int(self.frame)]
        if self.spawn:
            surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
                       