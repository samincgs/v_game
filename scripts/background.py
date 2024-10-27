import pygame
import math

class Background:
    def __init__(self, game):
        self.game = game
        self.angle = math.radians(-30)
        self.color = (50, 0, 46)
        self.pos = 0
        self.thickness = 20
        self.speed = 40
        
    def update(self):
        self.pos = (self.pos + self.speed * self.game.window.dt) % (self.thickness * 2)
    
    def render(self, surf):
        angle = math.sin(self.angle) / math.cos(self.angle)
        offset = angle * surf.get_width()
        for i in range(15):
            base_y = i * (self.thickness * 2) + self.pos
            pygame.draw.line(surf, self.color, (0, base_y), (surf.get_width(), base_y + offset), self.thickness)