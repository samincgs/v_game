import pygame
import math
import random


EFFECT_GROUPS = {
    'bow_sparks': {
        'base': [ # type, start angle, curve, speed, scale, decay_rate
            ['curved_spark', math.pi / 8, math.pi / 160, 3, 5, 0.4],
            ['curved_spark', -math.pi / 8, -math.pi / 160, 3, 5, 0.4],
            ['curved_spark', 0, 0, 3, 4, 0.2],
        ],
        'random': [
            [[[0, 0], [0, 0]], [math.pi / 4, -math.pi / 8], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[[0, 0], [0, 0]], [math.pi / 4, -math.pi / 8], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[[0, 0], [0, 0]], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ],
    },
    "arrow_sparks" : {
        'base': ['curved_spark', 0, 0, 4, 6, 0.6]
    },
    'random': [
            [[[0, 0], [0, 0]], [math.pi / 4, -math.pi / 8], [0, 0], [0, 0], [0, 0], [0, 0]],
        ],
}

class CurvedSpark:
    def __init__(self, pos, angle, curve, speed, scale, decay_rate=1, color=(255,255, 255)):
        self.pos = list(pos)
        self.angle = angle
        self.curve = curve
        self.speed = speed
        self.scale = scale
        self.decay_rate = decay_rate
        self.color = color
        
    def update(self, dt):
        dt *= 60  # Frame rate independence
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        self.angle += self.curve * self.speed * dt
        
        self.speed = max(0, self.speed - self.decay_rate * dt)
        
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        if self.speed:
            iterations = 5
            points = []
            temp_pos = self.pos.copy()
            temp_angle = self.angle
            
            for i in range(iterations):
                points.append((temp_pos[0] - offset[0], temp_pos[1] - offset[1]))
                temp_pos[0] += math.cos(temp_angle) * self.speed * self.scale / iterations
                temp_pos[1] += math.sin(temp_angle) * self.speed * self.scale / iterations
                temp_angle += self.curve * self.speed / iterations
            
            pygame.draw.lines(surf, self.color, False, points, 2)
            
class VFX:
    def __init__(self):
        self.effects = []
        
    def update(self, dt):
        for effect in self.effects.copy():
            kill = effect.update(dt)
            if kill:
                self.effects.remove(effect)
                
    def render(self, surf, offset=(0,0)):
        for effect in self.effects:
            effect.render(surf, offset=offset)
            
    def spawn_effect(self, effect_type, *args, **kwargs):
        if effect_type == 'curved_spark':
            self.effects.append(CurvedSpark(*args, **kwargs))

    def spawn_group(self, group_type, position, rotation, color=(255, 255, 255)):
        group_data = EFFECT_GROUPS[group_type]
        base_data = group_data['base']
        random_data = group_data.get('random', [])

        for i, effect_data in enumerate(base_data):
            effect_type = effect_data[0]
            args = [list(position)] + effect_data[1:]  # Set position as the first argument

            # Adjust angle with the rotation parameter
            args[1] += rotation

            # Apply random adjustments if available
            if i < len(random_data):
                random_variations = random_data[i]
                for j in range(len(random_variations)):
                    if isinstance(args[j], (int, float)):
                        args[j] += random.uniform(random_variations[j][0], random_variations[j][1])
                    elif isinstance(args[j], list) and len(args[j]) == 2:
                        args[j][0] += random.uniform(random_variations[j][0][0], random_variations[j][0][1])
                        args[j][1] += random.uniform(random_variations[j][1][0], random_variations[j][1][1])

            # Add the effect to the effects list
            self.spawn_effect(effect_type, *args, color=color)