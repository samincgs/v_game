import pygame
import time
import random
import sys
import os

from .config import config
from scripts.pgtools.utils import save_json

class Window:
    def __init__(self, game):
        pygame.init()
        
        self.game = game
        self.settings = config['settings']
        
        self.window = pygame.display.set_mode(self.resolution) 
        pygame.display.set_caption(self.settings['caption'])
        self.display = pygame.Surface(self.scaled_res)
        self.clock = pygame.time.Clock()
        
        pygame.mouse.set_visible(False)
                
        self.start_frame = time.time() 
        
        # incorporate delta time
        self.dt = 0.01
        
        self.screenshake = 0
        
        self.inventory_mode = False
        self.show_settings = False
    
    @property
    def resolution(self):
        return [int(v) for v in self.settings['window_resolution'].split('x')]
    
    @property
    def render_scale(self):
        return (self.resolution[0] / self.settings['base_res'][0], self.resolution[1] / self.settings['base_res'][1])
    
    @property
    def scaled_res(self):
        return (self.resolution[0] / self.render_scale[0], self.resolution[1] / self.render_scale[1])
    
    @property
    def fps(self):
        return 1 / self.dt if self.dt > 0 else 0
    
    @property
    def show_fps_index(self):
        return 0 if self.settings['show_fps'] == 'disabled' else 1
    
    @property
    def pause_state(self):
        return self.inventory_mode or self.show_settings or self.game.world.transition
    
    def quit_window(self):
        pygame.quit()
        sys.exit()
    
    def save_settings(self):
        save_json('data/config/settings.json', self.settings)
    
    def reload_window(self):
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        self.window = pygame.display.set_mode(self.resolution) 
    
    def create(self):
        self.clock.tick(60)
        
        self.dt = time.time() - self.start_frame
        self.start_frame = time.time()

        if (not self.inventory_mode) or self.game.world.transition:
            if self.game.input.pressing('quit'):
                self.show_settings = not self.show_settings
                self.game.renderer.settings_menu.reset()
        if (not self.show_settings) or self.game.world.transition:
            if self.game.input.pressing("inventory_toggle"):
                self.inventory_mode = not self.inventory_mode
        
        screenshake_offset = (0, 0)
        if self.screenshake:
            self.screenshake = max(0, self.screenshake - self.dt)
            screenshake_offset = (random.uniform(-self.screenshake, self.screenshake), random.uniform(-self.screenshake, self.screenshake))
        
        
        self.display.blit(self.game.assets.misc['cursor'], (self.game.input.mpos[0] - self.game.assets.misc['cursor'].get_width() // 2, self.game.input.mpos[1] - self.game.assets.misc['cursor'].get_height() // 2))
        self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), screenshake_offset)
        pygame.display.flip()
        self.display.fill(self.settings['bg_color'])
        
        
        
        
        