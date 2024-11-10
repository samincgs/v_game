import math

from .entity import Entity
from .weapon import Weapon

class Player(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.dash = 0
        self.aim_angle = 0
        self.inventory = {'weapons': [Weapon(game, 'golden_gun', self)]} # {'weapons' : [], 'skills': [], 'items': []}
        self.selected_weapon = 0
        
        self.last_collisions = {k : False for k in ['top', 'left', 'right', 'bottom']}
        self.frame_movement = [0, 0]
        
        self.add_weapon(Weapon(game, 'rifle', self)) # add second weapon
    
    @property
    def weapon(self):
        return self.inventory['weapons'][self.selected_weapon]
        
    def add_weapon(self, item): # TODO: Dont allow duplicate weapons
        for weapon in self.inventory['weapons']:
            if item.name == weapon.name:
                return    
        self.inventory['weapons'].append(item)
            
            
    
    def slot_weapon(self, direction):
        self.selected_weapon = (self.selected_weapon + direction) % len(self.inventory['weapons'])
    
    
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
        if self.game.input.mouse_states[self.weapon.trigger]:
            self.weapon.attack()
            
        if self.game.input.mouse_states['scroll_up']:
            self.slot_weapon(-1)
        if self.game.input.mouse_states['scroll_down']:
            self.slot_weapon(1)
        
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
            
        
            
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        self.weapon.render(surf, (self.center[0] - offset[0], self.center[1] - offset[1] + 2))
        
        
            
    