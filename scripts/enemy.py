import math
import random

from .entity import Entity
from .utils import normalize
from .item import create_item

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
        
        self.drops = [create_item(game, 'bat_wing', self) for i in range(random.randint(0, 2))]
                
    def update(self, dt):
        kill = super().update(dt)
        
        self.attack_timer += dt
        self.hover_timer += dt

        player = self.game.world.player

        self.velocity[0] = normalize(self.velocity[0], 100 * dt)
        self.velocity[1] = normalize(self.velocity[1], 100 * dt)

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
        self.target_offset_angle += 0.5 * dt 
        if self.target_offset_angle > 2 *  math.pi:  
            self.target_offset_angle = random.uniform(math.pi, 2 * math.pi) 
            
        target_pos = [player.pos[0] + math.cos(self.target_offset_angle) * self.hover_distance, player.pos[1] + math.sin(self.target_offset_angle) * self.hover_distance]

        target_pos[1] += math.sin(self.hover_timer * self.hover_frequency) * self.vertical_amplitude

        target_angle = self.get_angle(target_pos)
        distance_to_target = self.get_distance(target_pos)
                
        if distance_to_target > self.speed * dt:
            self.pos[0] += math.cos(target_angle) * self.speed * dt
            self.pos[1] += math.sin(target_angle) * self.speed * dt
        else:
            self.velocity[0] = 0
            self.velocity[1] = 0
        
        attack_angle = self.get_angle(player)
                
        if distance_to_target <= 150:
            if self.attack_timer > 6:
                self.attack_timer = 0
                self.game.world.projectile_manager.add_projectile(self.game, self.center, attack_angle, 140, 'bat_goo')
            
        return kill
       
ENEMIES = {
    'bat': Bat
}      
        
        
        
        
        
        
        