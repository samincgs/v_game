import pygame
import math


class Spark:
    def __init__(self, pos, speed, angle, curve, color=(255,255,255), decay_rate=1):
        self.pos = list(pos)
        self.speed = speed
        self.angle = angle
        self.curve = curve
        self.color = color
        self.decay_rate = decay_rate
        
    def update(self, dt):
        dt *= 60
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        
        self.angle += self.curve * self.speed * dt
        
        self.speed = max(0, self.speed - self.decay_rate * dt)
        
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        if self.speed:
            end_pos = (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], 
                       self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1])
            
            pygame.draw.line(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), end_pos, 2)
            
            
class SparkManager:
    def __init__(self, game):
        self.game = game
        self.sparks = []
    
    def add_spark(self, pos, angle, speed, curve, color=(255, 255, 255), decay_rate=1):
       self.sparks.append(Spark(pos, speed, angle, curve, color, decay_rate))
       
    def update(self, dt):
        for spark in self.sparks.copy():
            kill = spark.update(dt)
            if kill:
                self.sparks.remove(spark)
            
    def render(self, surf, offset=(0, 0)):
        for spark in self.sparks:
            spark.render(surf, offset=offset)
            