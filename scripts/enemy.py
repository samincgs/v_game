import math
import random

from scripts.entity import Entity
from scripts.pgtools.utils import normalize, get_angle, get_distance
from scripts.item import create_item

class Bat(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'bat')
        self.velocity = [0, 0]
        self.attack_timer = 0
        self.hover_timer = 0
        self.hover_distance = random.randint(50, 90)
        self.speed = random.randint(30, 70)
        self.vertical_amplitude = 6
        self.hover_frequency = random.randint(10, 30) / 10
        self.target_offset_angle = random.uniform(0, 2 * math.pi)  
        
        self.drops = [create_item(game, 'bat_wing', None) for i in range(random.randint(0, 2))]
                
    def update(self, dt):
        kill = super().update(dt)
        
        self.attack_timer += dt
        self.hover_timer += dt

        player = self.game.world.player

        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt

        self.velocity[0] = normalize(self.velocity[0], 150 * dt)
        self.velocity[1] = normalize(self.velocity[1], 150 * dt)
    
        self.target_offset_angle += 0.5 * dt 
        if self.target_offset_angle > 2 *  math.pi:  
            self.target_offset_angle = random.uniform(math.pi, 2 * math.pi) 
            
        target_pos = [player.pos[0] + math.cos(self.target_offset_angle) * self.hover_distance, player.pos[1] + math.sin(self.target_offset_angle) * self.hover_distance]

        target_pos[1] += math.sin(self.hover_timer * self.hover_frequency) * self.vertical_amplitude

        target_angle = get_angle(self, target_pos)
        distance_to_target = get_distance(self.pos, target_pos)
                
        if distance_to_target > self.speed * dt:
            self.pos[0] += math.cos(target_angle) * self.speed * dt
            self.pos[1] += math.sin(target_angle) * self.speed * dt
        else:
            self.velocity[0] = 0
            self.velocity[1] = 0
        
        attack_angle = get_angle(self, player)
                
        if distance_to_target <= 150:
            if self.attack_timer > 6:
                self.attack_timer = 0
                self.game.world.projectile_manager.add_projectile(self.game, owner=self, pos=self.center, rot=attack_angle, speed=140, p_type='bat_goo')
            
        return kill
       
ENEMIES = {
    'bat': Bat
}      
        
        
        
        
        
        
        