import pygame
import math

from .entity import Entity
from .weapon import Weapon
from .utils import outline

class Player(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.dash = 0
        self.aim_angle = 0
        self.weapon = Weapon(game, self, 'golden_gun')
        self.projectiles = []
        
        self.last_collisions = {k : False for k in ['top', 'left', 'right', 'bottom']}
        self.frame_movement = [0, 0]
        

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
        self.frame_movement[0] += 120 * direction
        
    def update(self, dt):
        self.frame_movement = self.velocity.copy()
        
        super().update(dt)
        self.air_timer += dt
          
        # normalize x axis movement
        if self.game.input.states['jump']:
            self.jump()
        if self.game.input.states['right']:
            self.move(1)
        if self.game.input.states['left']:
            self.move(-1)
        if self.game.input.states['reload']:
            self.weapon.reload()
        if self.game.input.mouse_states[self.weapon.config[self.weapon.type]['trigger']]:
            self.weapon.attack()
        
        self.velocity[1] = min(500, self.velocity[1] + dt * 700)
                
        self.frame_movement[0] *= dt
        self.frame_movement[1] *= dt
        
        self.last_collisions = self.collisions(self.game.world.tilemap, self.frame_movement)
        if self.last_collisions['bottom'] or self.last_collisions['top']:
            if self.last_collisions['bottom']:
                self.jumps = self.max_jumps
            self.velocity[1] = 0
            self.air_timer = 0
            
        if self.air_timer > 0.10:
            self.set_action('jump')
        elif self.frame_movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        # weapon
        angle = math.atan2(self.game.input.mpos[1] - self.center[1] + self.game.world.camera.pos[1], self.game.input.mpos[0] - self.center[0] + self.game.world.camera.pos[0])
        self.aim_angle = angle
        self.weapon.rotation = math.degrees(angle)
        
        if (self.weapon.rotation % 360 > 90) and (self.weapon.rotation % 360 < 270):
            self.flip[0] = True
        else:
            self.flip[0] = False 
        
        
        for proj in self.projectiles.copy():
            kill = proj.update(dt)
            proj.render(self.game.window.display, self.game.world.camera.pos)
            if kill:
                self.projectiles.remove(proj)
            
        
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        self.weapon.render(surf, (self.center[0] - offset[0], self.center[1] - offset[1] + 2))
        
        
            
    