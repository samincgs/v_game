import pygame
import math


class SparkLine:
    def __init__(self, pos, speed, angle, color=(255,255,255), decay_rate=1):
        self.pos = list(pos)
        self.speed = speed
        self.angle = angle
        self.color = color
        self.decay_rate = decay_rate
        
    def update(self, dt):
        dt *= 60
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt

        self.speed = max(0, self.speed - self.decay_rate * dt)
        
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        if self.speed:
            end_pos = (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], 
                       self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1])
            
            pygame.draw.line(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), end_pos, 2)
            
class CurvedSpark:
    def __init__(self, pos, angle, curve, speed, color=(255, 255, 255), decay_rate=0.1):
        self.pos = list(pos)  
        self.angle = angle  
        self.curve = curve  
        self.speed = speed  
        self.color = color  
        self.decay_rate = decay_rate 

    def update(self, dt):
        dt *= 60  # scale dt for frame independence
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        
        self.angle += self.curve * self.speed * dt
        
        self.speed = max(0, self.speed - self.decay_rate * dt)
        
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        if self.speed:
            end_pos1 = (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0],self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1])
            end_pos2 = (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 1.5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi / 2) * self.speed * 1.5 - offset[1])
            
            pygame.draw.polygon(surf, self.color, [(self.pos[0] - offset[0], self.pos[1] - offset[1]), end_pos1, end_pos2], 2)
                      
class SparkManager:
    def __init__(self):
        self.sparks = []
    
    def add_spark(self, s_type, pos, angle, speed, curve=None, color=(255, 255, 255), decay_rate=1):
        if s_type == 'spark_line':
            self.sparks.append(SparkLine(pos, speed, angle, color, decay_rate))
        elif s_type == 'spark_curve':
            self.sparks.append(CurvedSpark(pos, angle, curve, speed, color, decay_rate))
       
    def update(self, dt):
        for spark in self.sparks.copy():
            kill = spark.update(dt)
            if kill:
                self.sparks.remove(spark)
            
    def render(self, surf, offset=(0, 0)):
        for spark in self.sparks:
            spark.render(surf, offset=offset)
            