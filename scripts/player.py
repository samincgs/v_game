import math
import random

from .entity import Entity
from .inventory import Inventory
from .utils import normalize
from .spark import CurvedSpark
from .skill import DashSkill


class Player(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.skills =[DashSkill(game, self, 'dash')]
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
    
    def pickup_item(self, item):
        item.owner = self
        item_type = 'weapons' if 'weapon' in item.tags else 'items'
        self.inventory.add_item(item, item_type)
                   
    def slot_weapon(self, direction):
        active_weapons = self.inventory.get_active_weapons()
        if active_weapons:
            self.selected_weapon = (self.selected_weapon + direction) % len(active_weapons)
                
    def jump(self):
        if self.jumps:
            self.velocity[1] = -250
            self.jumps -= 1
    
    def dash(self):
        if not self.dash_timer and self.dashes > 0:
            self.dashes -= 1
            self.dash_timer = 0.2
            self.velocity[0] = math.cos(self.aim_angle) * 450 
            self.velocity[1] = math.sin(self.aim_angle) * 450 
            for i in range(12):
                self.game.world.spark_manager.sparks.append(CurvedSpark(self.center.copy(), math.pi + self.aim_angle + random.uniform(-math.pi / 6, math.pi / 6), random.randint(30,80) / 10, random.randint(-10, 10) / 100, scale=2, decay_rate=random.randint(40, 70) / 100))
            
    # direction is 1 or 0 or -1
    def move(self, direction):
        if direction < 0:
            self.flip[0] = True
        if direction > 0:
            self.flip[0] = False
        self.frame_movement[0] += 120 * direction
    
        
    def update(self, dt):
        self.frame_movement = self.velocity.copy()
            
        r = super().update(dt)
        self.air_timer += dt
                
        if not self.game.world.inventory_mode:
            
            # player controls
            if self.game.input.mouse_states['right_click']:
                self.skills[0].use()
            if self.game.input.states['jump']:
                self.jump()
            if self.game.input.states['right']:
                self.move(1)
            if self.game.input.states['left']:
                self.move(-1)
            if self.weapon:
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
                        
        # item pickup
        for entity in self.game.world.entities.entities:
            if self.rect.colliderect(entity.rect):
                if entity.type == 'item':
                    entity.dead = True
                    self.pickup_item(entity.item_data)
                    self.game.world.item_notifications.add_item_notif(entity.item_data)
                    
        if self.weapon:
            self.weapon.update()
        
        # weapon
        angle = math.atan2(self.game.input.mpos[1] - self.center[1] + self.game.world.camera.pos[1], self.game.input.mpos[0] - self.center[0] + self.game.world.camera.pos[0])
        self.aim_angle = angle
        if self.weapon:
            self.weapon.rotation = math.degrees(angle)
        
            if (self.weapon.rotation % 360 > 90) and (self.weapon.rotation % 360 < 270):
                self.flip[0] = True
            else:
                self.flip[0] = False 
        
        
              
        for skill in self.skills:
            skill.update(dt)     
                
        
                
        return r
   
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        if self.weapon:
            self.weapon.render(surf, (self.center[0] - offset[0], self.center[1] - offset[1] + 2))
            
        for skill in self.skills:
            skill.render(surf, offset=offset)
        
       
        
        
        
            
    