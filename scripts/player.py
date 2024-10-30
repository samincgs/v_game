import pygame

from .entity import Entity

class Player(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.dash = 0
        self.aim_angle = 0
        
        self.last_collisions = {k : False for k in ['top', 'left', 'right', 'bottom']}
        self.frame_motion = [0, 0]
        

    def jump(self):
        if self.jumps:
            self.velocity[1] = -300
            self.jumps -= 1
    
    # direction is 1 or 0 or -1
    def move(self, direction):
        if direction > 0:
            self.flip[0] = False
        if direction < 0:
            self.flip[0] = True
        self.frame_motion[0] += 120 * direction
        
    def update(self, dt):
        self.frame_motion = self.velocity.copy()
        
        super().update(dt)
        self.air_timer += dt
        
        # normalize x axis movement
        if self.game.input.states['jump']:
            self.jump()
        if self.game.input.states['right']:
            self.move(1)
        if self.game.input.states['left']:
            self.move(-1)
            
        self.velocity[1] = min(500, self.velocity[1] + dt * 700)
        
        self.frame_motion[0] *= dt
        self.frame_motion[1] *= dt
        
        self.last_collisions = self.collisions(self.game.world.tilemap, self.frame_motion)
        if self.last_collisions['bottom'] or self.last_collisions['top']:
            if self.last_collisions['bottom']:
                self.jumps = self.max_jumps
            self.velocity[1] = 0
            self.air_timer = 0
            
            
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
            
    