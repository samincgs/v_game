import pygame
import sys

from .config import config

class Input:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.mouse_states = {}
        self.config = config['input']
        
        self.mpos = (0, 0)
        self.show_fps = False
        
        pygame.mouse.set_visible(False)
        
        self.create_inputs()
    
    def create_inputs(self):
        for binding in self.config:
            if self.config[binding]['binding'][0] == 'keyboard':
                self.states[binding] = False
            else:
                self.mouse_states[binding] = False
    
    def reset(self):
        for binding in self.config:
            if self.config[binding]['trigger'] == 'press':
                if self.config[binding]['binding'][0] == 'keyboard':
                    self.states[binding] = False
                elif self.config[binding]['binding'][0] == 'mouse':
                        self.mouse_states[binding] = False
                        
      
    def update(self):
                
        mpos = pygame.mouse.get_pos()
        self.mpos = (int(mpos[0] / self.game.window.render_scale), int(mpos[1] / self.game.window.render_scale))
            
        self.reset()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for binding in self.config:
                    if self.config[binding]['binding'][0] == 'mouse':
                        if self.config[binding]['trigger'] in ['hold', 'press']:
                            if event.button == self.config[binding]['binding'][1]:
                                self.mouse_states[binding] = True                     
            if event.type == pygame.MOUSEBUTTONUP:
                for binding in self.config:
                    if self.config[binding]['binding'][0] == 'mouse':
                        if self.config[binding]['trigger'] in ['hold']:
                            if event.button == self.config[binding]['binding'][1]:
                                self.mouse_states[binding] = False    
            if event.type == pygame.KEYDOWN:
                for binding in self.config:
                    if self.config[binding]['binding'][0] == 'keyboard':
                        if self.config[binding]['trigger'] in ['hold', 'press']:
                            if event.key == self.config[binding]['binding'][1]:
                                self.states[binding] = True   
            if event.type == pygame.KEYUP:
                for binding in self.config:
                    if self.config[binding]['binding'][0] == 'keyboard':
                        if self.config[binding]['trigger'] in ['hold']:
                            if event.key == self.config[binding]['binding'][1]:
                                self.states[binding] = False 
                        
        if self.states['quit']:
            pygame.quit()
            sys.exit()
        if self.states['fps']:
            self.show_fps = not self.show_fps
        if self.states['screen_toggle']:
            self.game.window.toggle_window()
                
                