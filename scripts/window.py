import pygame
import time

from .config import config

class Window:
    def __init__(self, game):
        pygame.init()
        
        self.game = game
        self.config = config['window']
        
        pygame.display.set_caption(self.config['caption'])
        
        self.clock = pygame.time.Clock()
        
        self.window = pygame.display.set_mode(self.config['scaled_res'], pygame.SCALED) # pygame.RESIZABLE
        self.display = pygame.Surface(self.config['base_res'])
        
        self.render_scale = self.config['render_scale']
        
        self.start_frame = time.time()
        
        # incorporate delta time
        self.dt = 0.01
    
    @property
    def fps(self):
        return 1 / self.dt if self.dt > 0 else 0
    
    def create(self):
        # self.clock.tick(120)
        
        self.dt = time.time() - self.start_frame
        self.start_frame = time.time()
        
        self.display.blit(self.game.assets.misc['cursor'], (self.game.input.mpos[0] - self.game.assets.misc['cursor'].get_width() // 2, self.game.input.mpos[1] - self.game.assets.misc['cursor'].get_height() // 2))
        self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
        pygame.display.update()
        
        self.display.fill(config['window']['bg_color'])
        
        
        
        
        