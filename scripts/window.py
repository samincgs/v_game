import pygame
import time

from .config import config

class Window:
    def __init__(self, game):
        pygame.init()
        
        self.game = game
        self.config = config['window']
                
        self.window = pygame.display.set_mode(self.config['scaled_res']) # pygame.RESIZABLE
        pygame.display.set_caption(self.config['caption'])
        self.display = pygame.Surface(self.config['base_res'])
        self.clock = pygame.time.Clock()
        
        self.render_scale = self.config['render_scale']
        
        self.start_frame = time.time() 
        
        # incorporate delta time
        self.dt = 0.01
        
        self.scaled = False
    
    @property
    def fps(self):
        return 1 / self.dt if self.dt > 0 else 0
    
    def toggle_window(self):
        self.scaled = not self.scaled
        if self.scaled:
            self.window = pygame.display.set_mode(self.config['scaled_res'], pygame.SCALED)
        else:
            self.window = pygame.display.set_mode(self.config['scaled_res'])  
    
    def create(self):
        self.clock.tick(120)
        
        self.dt = time.time() - self.start_frame
        self.start_frame = time.time()
        
        self.display.blit(self.game.assets.misc['cursor'], (self.game.input.mpos[0] - self.game.assets.misc['cursor'].get_width() // 2, self.game.input.mpos[1] - self.game.assets.misc['cursor'].get_height() // 2))
        self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0, 0))
        pygame.display.update()
        # self.clock.tick(60)
        self.display.fill(self.config['bg_color'])
        
        
        
        
        