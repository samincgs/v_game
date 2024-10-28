import pygame
import sys

from .config import config

class InputManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.mouse_states = {}
        
        self.mpos = (0, 0)
        
        pygame.mouse.set_visible(False)
        
        self.create_inputs()
    
    def create_inputs(self):
        for binding in config['input']:
            if config['input'][binding]['binding'][0] == 'keyboard':
                self.states[binding] = False
            else:
                self.mouse_states[binding] = False
      
    def update(self):
        
        mpos = pygame.mouse.get_pos()
        self.mpos = (int(mpos[0] / self.game.window.render_scale), int(mpos[1] / self.game.window.render_scale))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for binding in config['input']:
                    if config['input'][binding]['binding'][0] == 'mouse':
                        if config['input'][binding]['trigger'] in ['hold', 'press']:
                            if event.button == config['input'][binding]['binding'][1]:
                                self.mouse_states[binding] = True                     
            if event.type == pygame.MOUSEBUTTONUP:
                for binding in config['input']:
                    if config['input'][binding]['binding'][0] == 'mouse':
                        if config['input'][binding]['trigger'] in ['hold', 'press']:
                            if event.button == config['input'][binding]['binding'][1]:
                                self.mouse_states[binding] = False    
            if event.type == pygame.KEYDOWN:
                for binding in config['input']:
                    if config['input'][binding]['binding'][0] == 'keyboard':
                        if config['input'][binding]['trigger'] in ['hold', 'press']:
                            if event.key == config['input'][binding]['binding'][1]:
                                self.states[binding] = True   
            if event.type == pygame.KEYUP:
                for binding in config['input']:
                    if config['input'][binding]['binding'][0] == 'keyboard':
                        if config['input'][binding]['trigger'] in ['hold', 'press']:
                            if event.key == config['input'][binding]['binding'][1]:
                                self.states[binding] = False 
                        
            if self.states['esc']:
                pygame.quit()
                sys.exit()