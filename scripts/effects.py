import pygame

class Goo:
    def __init__(self, game, img, pos, rot, duration=3, decay_rate=0.5):
        self.game = game
        self.img = img
        self.pos = list(pos)
        self.rot = rot
        self.duration = duration
        self.decay_rate = decay_rate
        
        self.img = pygame.transform.rotate(self.img, self.rot)
        self.rect = pygame.Rect(self.pos[0] - self.img.get_width() // 2, self.pos[1] - self.img.get_height() // 2, *self.img.get_size())
        
    def update(self, dt):
        self.duration = max(0, self.duration - self.decay_rate * dt)
        
        if self.rect.colliderect(self.game.world.player):
            pass
        
        return not self.duration
    
    def render(self, surf, offset=(0, 0)):
        if self.duration:    
            surf.blit(self.img, (self.pos[0] - self.img.get_width() // 2 - offset[0] + 2, self.pos[1] - self.img.get_height() // 2 - offset[1] + 1))