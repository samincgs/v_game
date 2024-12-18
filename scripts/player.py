import math
import random

from .entity import Entity
from .inventory import Inventory
from .utils import clip, normalize

class Player(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.dash_timer = 0
        self.dash_info = []
        self.aim_angle = 0
        self.inventory = Inventory()       
        self.selected_weapon = 0
        
        self.last_collisions = {k : False for k in ['top', 'left', 'right', 'bottom']}
        self.frame_movement = [0, 0]
        
    @property
    def weapon(self):
        active_weapons = self.inventory.get_active_weapons()
        if active_weapons:
            return active_weapons[self.selected_weapon]
                    
    def slot_weapon(self, direction):
        active_weapons = self.inventory.get_active_weapons()
        if active_weapons:
            self.selected_weapon = (self.selected_weapon + direction) % len(active_weapons)
            
    def jump(self):
        if self.jumps:
            self.velocity[1] = -300
            self.jumps -= 1
    
    def dash(self):
        if not self.dash_timer:
            self.dash_timer = 0.2
            self.velocity[0] = math.cos(self.aim_angle) * 450
            self.velocity[1] = math.sin(self.aim_angle) * 450
            
  
    # direction is 1 or 0 or -1
    def move(self, direction):
        if direction > 0:
            self.flip[0] = False
        if direction < 0:
            self.flip[0] = True
        self.frame_movement[0] += 120 * direction
    
        
    def update(self, dt):
        self.frame_movement = self.velocity.copy()
        
        kill = super().update(dt)
        self.air_timer += dt
        self.dash_timer = max(0, self.dash_timer - dt)
        
        if self.dash_timer:
            if random.randint(1, 3) == 1:
                self.dash_info.append({'pos': self.pos.copy(), 'img': self.img.copy()})
        else:
            self.dash_info = []

        if not self.game.world.inventory_mode:
            # player controls
            if self.game.input.mouse_states['right_click']:
                self.dash()
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
        
            
        if self.game.input.states["inventory_toggle"]:
            self.game.world.inventory_mode = not self.game.world.inventory_mode
        
        
        self.velocity[0] = normalize(self.velocity[0], 550 * dt)
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
            
        return kill
   
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        self.weapon.render(surf, (self.center[0] - offset[0], self.center[1] - offset[1] + 2))
        for dash in self.dash_info:
            img = dash['img']
            img.set_alpha(45)
            surf.blit(img, (dash['pos'][0] - offset[0], dash['pos'][1] - offset[1]))
        # pygame.draw.rect(surf, (0, 255, 0), pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], *self.size), 1) # debug
        
            
    