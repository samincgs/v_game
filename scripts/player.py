import math
import pygame

from scripts.physics_entity import PhysicsEntity
from scripts.inventory import Inventory
from scripts.old.utils import normalize


class Player(PhysicsEntity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.air_timer = 0
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.aim_angle = 0
        self.inventory = Inventory()       
        self.selected_weapon = 0
        self.dropthrough = True
        self.dropthrough_timer = 0
        self.grass_effect = (6, 12)
               
    @property
    def weapon(self):
        active_weapons = self.inventory.get_active_weapons()
        if active_weapons:
            return active_weapons[self.selected_weapon]

    def pickup_item(self, item):
        item.dead = True
        item.item_data.owner = self
        item_type = 'weapons' if 'weapon' in item.item_data.tags else 'items'
        self.inventory.add_item(item.item_data, item_type)
                   
    def slot_weapon(self, direction):
        active_weapons = self.inventory.get_active_weapons()
        if active_weapons:
            self.selected_weapon = (self.selected_weapon + direction) % len(active_weapons)
    
    def weapon_hotkeys(self):
        active_weapons_len = len(self.inventory.get_active_weapons())
        for key in '1234':
            hotkey = int(key) - 1
            if self.game.input.pressing(key) and hotkey < active_weapons_len:
                self.selected_weapon = hotkey
               
    def jump(self):
        if self.jumps:
            self.velocity[1] = -250
            self.jumps -= 1

    # direction is 1 or 0 or -1
    def move(self, direction):
        if direction < 0:
            self.flip[0] = True
        if direction > 0:
            self.flip[0] = False
        self.frame_movement[0] += 135 * direction
    
        
    def update(self, dt):      
        
        if self.active_animation:
            self.active_animation.update(dt)
                
        self.air_timer += dt
        self.dropthrough_timer = max(0, self.dropthrough_timer - dt)
                
        if self.pos[1] > 600 and self.air_timer > 3:
            self.air_timer = 0
            self.game.world.transition = 1

        if not self.game.world.inventory_mode and not self.game.world.transition:
            if self.game.input.pressing('jump'):
                self.jump()
        
        self.frame_movement = self.velocity.copy()
          
        if not self.game.world.inventory_mode and not self.game.world.transition:
            # player controls
            for i, skill in enumerate(self.inventory.get_active_skills()):
                if self.game.input.clicking('skill_1') and i == 0:
                    skill.use()
            if self.game.input.holding('right'):
                self.move(1)
            if self.game.input.holding('left'):
                self.move(-1)
            if self.game.input.pressing('drop') and not self.dropthrough_timer:
                self.dropthrough_timer = 0.35
            if self.weapon:
                if self.game.input.pressing('reload'):
                    self.weapon.reload()
                if self.weapon.input_type == 'press':
                    if self.game.input.clicking(self.weapon.trigger):
                        self.weapon.attack()
                if self.weapon.input_type == 'hold':
                    if self.game.input.holding(self.weapon.trigger):
                        self.weapon.attack()
                if self.game.input.clicking('scroll_up'):
                    self.slot_weapon(-1)
                if self.game.input.clicking('scroll_down'):
                    self.slot_weapon(1)
                self.weapon_hotkeys()
        
            
        if self.game.input.pressing("inventory_toggle"):
            self.game.world.inventory_mode = not self.game.world.inventory_mode
        
        self.velocity[0] = normalize(self.velocity[0], 550 * dt)
        self.velocity[1] = min(500, self.velocity[1] + dt * 700)
        
            
        self.frame_movement[0] *= dt
        self.frame_movement[1] *= dt
        
        if self.air_timer > 0.10:
            self.set_action('jump')
        elif self.frame_movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        self.physics_movement(self.game.world.tilemap, self.frame_movement)
        if self.collision_directions['down'] or self.collision_directions['up']:
            if self.collision_directions['down']:
                self.jumps = self.max_jumps
            self.velocity[1] = 0
            self.air_timer = 0
            
        if self.weapon:
            self.weapon.update()
        
        # weapon
        angle = math.atan2(self.game.input.mpos[1] - self.center[1] + self.game.world.camera.pos[1], self.game.input.mpos[0] - self.center[0] + self.game.world.camera.pos[0])
        self.aim_angle = angle
        if self.weapon:
            self.weapon.rotation = math.degrees(angle)

            if ((self.weapon.rotation % 360 > 90) and (self.weapon.rotation % 360 < 270)):
                self.flip[0] = True
            else:
                self.flip[0] = False 
           
        for skill in self.inventory.get_active_skills():
            skill.update(dt)      
        
        force_point = (self.rect.centerx, self.rect.bottom)
        self.game.world.grass_manager.apply_bend(force_point, self.grass_effect[0], self.grass_effect[1])    
        
        return self.dead
   
    def render(self, surf, offset=(0, 0)):        
        dash_skill = [skill for skill in self.inventory.get_active_skills() if skill.skill_name == 'dash']
        if len(dash_skill):
            dash_skill = dash_skill[0]
            if not (dash_skill and dash_skill.dash_timer):
                super().render(surf, offset=self.game.world.camera.float_pos)
        else:
            super().render(surf, offset=self.game.world.camera.float_pos)
        if self.weapon:
            self.weapon.render(surf, offset=offset)
        for skill in self.inventory.get_active_skills():
            skill.render(surf, offset=offset)       
        
        
        
            
    