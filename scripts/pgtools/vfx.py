import math
import pygame

from .entities import Entity

class VFX:
    def __init__(self, game):
        self.game = game
        
        self.sparks = []
        self.circles = []
        self.action_animations = []
    
    def reset(self):
        self.sparks.clear()
        self.circles.clear()
        self.action_animations.clear()
    
    def add_spark(self, pos, angle, speed, decay_rate=2, custom_color=None):
        self.sparks.append(Spark(pos, angle, speed, decay_rate, custom_color))
        
    def add_anim(self, pos, a_type, size=(1, 1)):
        self.action_animations.append(ActionAnimation(self.game, pos, size, a_type))
        
    def update(self, dt, custom_func_sparks=None):
        for spark in self.sparks.copy():
            kill = spark.update(dt)
            if custom_func_sparks:
                kill = kill or custom_func_sparks(spark)
            if kill:
                self.sparks.remove(spark)
                
        for anim in self.action_animations.copy():
            kill = anim.update(dt)
            if kill:
                self.action_animations.remove(anim)
                
        for circle in self.circles.copy():
            kill = circle.update(dt)
            if kill:
                self.circles.remove(circle)
                
    def render(self, surf, offset=(0, 0)):
        for spark in self.sparks:
            spark.render(surf, offset=offset)
        for anim in self.action_animations:
            anim.render(surf, offset=offset)
        for circle in self.circles:
            circle.render(surf, offset=offset)
        
class Spark:
    def __init__(self, pos, angle, speed, decay_rate=2, custom_color=None):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.decay_rate = decay_rate
        self.custom_color = custom_color
            
    def update(self, dt):
        
        self.pos[0] += math.cos(self.angle) * self.speed * dt
        self.pos[1] += math.sin(self.angle) * self.speed * dt
        
        self.speed -= self.decay_rate * dt
        if self.speed <= 0:
            return True 
        

    def render(self, surf, offset=(0, 0)):  
        render_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])      
        points = [
            (render_pos[0] + math.cos(self.angle) * self.speed * 0.05, render_pos[1] + math.sin(self.angle) * self.speed * 0.05),
            (render_pos[0] + math.cos(self.angle + math.pi / 2) * self.speed * 0.01, render_pos[1] + math.sin(self.angle + math.pi / 2) * self.speed * 0.01),
            (render_pos[0] + math.cos(self.angle + math.pi) * self.speed * 0.05, render_pos[1] + math.sin(self.angle + math.pi) * self.speed * 0.05),
            (render_pos[0] + math.cos(self.angle - math.pi / 2) * self.speed * 0.01, render_pos[1] + math.sin(self.angle - math.pi / 2) * self.speed * 0.01),
        ]
        
        pygame.draw.polygon(surf, self.custom_color if self.custom_color else (255, 255, 255), points=points)
        
        
class Circle:
    def __init__(self, game, pos, speed, radius, color, width, decay_rate):
        self.game = game
        self.pos = list(pos)
        self.speed = speed
        self.radius = radius
        self.color = color
        self.width = width
        self.decay_rate = decay_rate
        
    def update(self, dt):
        self.radius += self.speed
        self.width -= self.decay_rate
        
        if self.width <= 0:
            return True
        
    def render(self, surf, offset=(0, 0)):
        pygame.draw.circle(surf, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1]), int(self.radius), max(1, int(self.width)))
    

class ActionAnimation(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        
    def update(self, dt):
        super().update(dt)
        
        if self.active_animation.finished:
            return True
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))