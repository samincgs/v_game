import pygame
import math
            
class Spark:
    def __init__(self, pos, angle, speed, color=(255, 255, 255), decay_rate=0.1):
        self.pos = list(pos)  
        self.angle = angle  
        self.speed = speed  
        self.color = color  
        self.decay_rate = decay_rate 

    def update(self, dt):
        dt *= 60  # scale dt for frame independence
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        
        self.speed = max(0, self.speed - self.decay_rate * dt)
        
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        pass

class CurvedSpark(Spark):
    def __init__(self, pos, angle, speed, curve, scale=2, color=(255, 255, 255), decay_rate=0.1):
        super().__init__(pos, angle, speed, color, decay_rate)
        self.curve = curve
        self.scale = scale
        
    def update(self, dt):
        self.angle += self.curve * self.speed * dt
        super().update(dt)
        
    def render(self, surf, offset=(0, 0)):
        if self.speed:
            spark_point = (self.pos[0] + math.cos(self.angle) * self.speed * self.scale - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * self.scale - offset[1])
            pygame.draw.line(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), end_pos=spark_point, width=2)
    
            
class SparkManager:
    def __init__(self):
        self.sparks = []
           
    def update(self, dt):
        for spark in self.sparks.copy():
            kill = spark.update(dt)
            if kill:
                self.sparks.remove(spark)
            
    def render(self, surf, offset=(0, 0)):
        for spark in self.sparks:
            spark.render(surf, offset=offset)
            