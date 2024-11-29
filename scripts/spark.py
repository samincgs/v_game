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
    def __init__(self, pos, angle, speed, curve, scale=3, color=(255, 255, 255), decay_rate=0.1):
        super().__init__(pos, angle, speed, color, decay_rate)
        self.curve = curve
        self.scale = scale
        
    def update(self, dt):
        super().update(dt)
        self.angle += self.curve * self.speed * dt
        
    def render(self, surf, offset=(0, 0)):
        pass
        

            
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
            