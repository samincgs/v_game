import pygame
import math
import random

class Background:
    def __init__(self, game):
        self.game = game
        self.angle = math.radians(-30)
        self.color = (30, 29, 126)
        self.pos = 0
        self.thickness = 20
        self.speed = 30
        
        self.squares = []
        
        
    def update(self):
        
        if random.randint(1, 40) == 1:
            self.squares.append(
                Square([random.randint(0, self.game.window.display.get_width()), -60], 
                        rot=random.randint(0, 359),   
                        rot_speed=random.uniform(2, 4),  
                        speed=random.uniform(1, 1.5),               
                        decay_rate=random.uniform(0.005, 0.05),            
                        size=random.randint(5, 15))
                        )
        for square in self.squares:
            kill = square.update(1/60)
            if kill:
                self.squares.remove(square)
        
        self.pos += (self.speed * self.game.window.dt)
        self.pos = self.pos % (self.thickness * 2)
        
            
    
    def render(self, surf):       
        
            
        # background
        angle = math.sin(self.angle) / math.cos(self.angle)  
        offset = angle * surf.get_width()
        for i in range(15):
            base_y = i * (self.thickness * 2) + self.pos
            pygame.draw.line(surf, self.color, (0, base_y), (surf.get_width(), base_y + offset), self.thickness)
            
        for square in self.squares:
            square.render(surf)

class Square:
    def __init__(self, pos, rot, rot_speed, speed, size, decay_rate):
        self.pos = list(pos)
        self.rot = math.radians(rot)
        self.rot_speed = math.radians(rot_speed)
        self.speed = speed
        self.size = size
        self.decay_rate = decay_rate
        self.color = (0, 0, 0)
        
    def update(self, dt):
        self.pos[1] += self.speed * dt
        self.rot += self.rot_speed
        self.size -= self.decay_rate
        
        if self.size <= 0:
            return True
        
    def vector_move(self, pos, angle, amt):
        new_pos = (pos[0] * math.cos(angle) * amt, pos[1] * math.sin(angle) * amt)
        return new_pos
    
    def render(self, surf, offset=(0, 0)):
        points = [
            self.vector_move((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.rot, self.size),
            self.vector_move((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.rot + math.radians(90), self.size),
            self.vector_move((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.rot + math.radians(180), self.size),
            self.vector_move((self.pos[0] - offset[0], self.pos[1] - offset[1]), self.rot + math.radians(270), self.size),
        ]
        
        pygame.draw.polygon(surf, self.color, points=points, width=6)
        
