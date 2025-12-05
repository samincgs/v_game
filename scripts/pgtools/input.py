import pygame
import sys

INPUT_MAP = {
    'mouse': {
        'shoot': 1,
        'attack': 1,
        'dash': 3,
        'scroll_up': 4,
        'scroll_down': 5
        },
    'keyboard': {
        'left': 97,
        'right': 100,
        'jump': 32,    
        'reload': 114,
        'up': 119,     
        'down': 115,
        'inventory_toggle': 101,
        'shift': 1073742049,
        'quit': 27,
        'fps': 9,
        'screen_toggle': 96,
        'equip': 122,
        '1': 49,
        '2': 50,
        '3': 51,
        '4': 52,
        'collect': 102,
    }
}

class InputData:
    def __init__(self, input_type, id):
        self.type = input_type
        self.id = id
        
        self.held = False
        self.pressed = False
        self.clicked = False
              
    def press(self):
        self.held = True
        if self.type == 'mouse':
            self.clicked = True
        if self.type == 'keyboard':
            self.pressed = True
        
    def release(self):
        self.pressed = False
        self.held = False
        self.clicked = False
        
    def reset(self):
        self.pressed = False
        self.clicked = False
    
class Input:
    def __init__(self, render_scale, input_map=INPUT_MAP):
        self.render_scale = render_scale
        self.input_map = input_map
        
        self.keyboard = {key: InputData('keyboard', self.input_map['keyboard'][key]) for key in self.input_map['keyboard']}
        self.mouse = {btn: InputData('mouse', self.input_map['mouse'][btn]) for btn in self.input_map['mouse']}
        self.mpos = (0, 0)
    
    def pressing(self, key):
        return self.keyboard[key].pressed
     
    def pressing_any_key(self):
        return True if any([key.pressed for key in self.keyboard.values()]) else False
    
    def holding(self, key):
        if key in INPUT_MAP['keyboard']:
            return self.keyboard[key].held
        else:
            return self.mouse[key].held
    
    def clicking(self, btn):
        return self.mouse[btn].clicked
    
    def reset(self):
        for trigger in self.keyboard:
            self.keyboard[trigger].reset()
        for click in self.mouse:
            self.mouse[click].reset()
    
    def update(self):
                
        self.mpos = pygame.mouse.get_pos()
        self.mpos = (self.mpos[0] // self.render_scale, self.mpos[1] // self.render_scale)
        
        self.reset()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.mouse:
                    if event.button == self.mouse[btn].id:
                        self.mouse[btn].press()
            if event.type == pygame.MOUSEBUTTONUP:
                for btn in self.mouse:
                    if event.button == self.mouse[btn].id and (self.mouse[btn].id not in [4, 5]): # make sure it doesn't release on scroll
                        self.mouse[btn].release()
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                for key in self.keyboard:
                    if event.key == self.keyboard[key].id:
                        self.keyboard[key].press() 
            if event.type == pygame.KEYUP:  
                for key in self.keyboard:
                    if event.key == self.keyboard[key].id:
                        self.keyboard[key].release()
                        
                        
                
        
        