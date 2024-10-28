import pygame
import time

from .config import config

class Window:
    def __init__(self, game):
        self.game = game
        
        pygame.init()
        pygame.display.set_caption(config['window']['caption'])
         
        self.window = pygame.display.set_mode(config['window']['scaled_res'])
        self.display = pygame.Surface(config['window']['base_res'])
        self.render_scale = config['window']['render_scale']
        
        # incorporate delta time
        self.dt = 0
        self.last_time = time.time()
        
    def create(self):
        self.display.blit(self.game.assets.misc['cursor'], (self.game.input.mpos[0] - self.game.assets.misc['cursor'].get_width() // 2, self.game.input.mpos[1] - self.game.assets.misc['cursor'].get_height() // 2))
        self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
        
        pygame.display.update()
        self.display.fill(config['window']['bg_color'])
        
        self.dt = time.time() - self.last_time
        self.last_time = time.time()
        
        
        
        