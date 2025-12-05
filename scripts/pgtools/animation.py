import os

from .utils import load_imgs_list, load_json, save_json

ANIMATIONS_PATH = 'data/images/animations/'
COLORKEY = (0, 0, 0)

class Animation:
    def __init__(self, config, images, anim_state):
        self.config = config
        self.images = images
        self.anim_state = anim_state
        self.animation = self.config['animations'][self.anim_state]
        self.frame = 0
        self.frame_index = 0
        self.finished = False
    
    @property
    def entity_id(self):
        return self.config['id']
         
    @property
    def img(self):
        return self.images[self.frame_index]
    
    @property
    def type(self):
        return self.animation['type']
    
    @property
    def duration(self):
        return sum(self.animation['frames'])
    
    @property
    def outline(self):
        return self.animation['outline']
    
    def copy(self):
        return Animation(self.config, self.images, self.anim_state)
        
    def update(self, dt):
        self.frame += dt * 60 * self.animation['speed']
        if self.animation['loop']:
            if self.frame > self.duration:
                self.frame -= self.duration
                                
        self.frame_index = int(self.frame / self.duration * len(self.animation['frames']))
        self.frame_index = min(self.frame_index, len(self.animation['frames']) - 1)
        if self.frame_index >= len(self.animation['frames']) - 1:
            if not self.animation['loop']:
                self.finished = True
        
class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.generate_configs() # save config if it isnt there
        self.load_configs()
    
    @property
    def animation_ids(self):
        return [anim.split('/')[0] for anim in list(self.animations)]
    
    def load_configs(self):
        # load animations
        for entity_id in os.listdir(ANIMATIONS_PATH):
            entity_path = ANIMATIONS_PATH + entity_id
            if not os.path.isdir(entity_path):  
                continue
            
            config_path = entity_path + '/' + 'config.json'
            if not os.path.isfile(config_path):
                continue
            
            config = load_json(config_path)
            
            for anim_state in os.listdir(entity_path):
                anim_path = entity_path + '/' + anim_state
                if os.path.isdir(anim_path):  
                    anim_id = entity_id + '/' + anim_state
                    self.animations[anim_id] = Animation(config, load_imgs_list(anim_path), anim_state)
              
    def generate_configs(self):
        if not os.path.isdir(ANIMATIONS_PATH):
            os.mkdir(ANIMATIONS_PATH)  
        
        for entity_id in os.listdir(ANIMATIONS_PATH):  
            entity_path = ANIMATIONS_PATH + entity_id 
            if not os.path.isdir(entity_path):
                continue
            
            config_path = entity_path + '/' + 'config.json'
            config = {}
            
            if os.path.isfile(config_path):
                config = load_json(config_path)
            
            if 'id' not in config:
                config['id'] = entity_id
            if 'animations' not in config:
                config['animations'] = {}
                
            generate_config = False
                
            for anim_state in os.listdir(entity_path):
                anim_path = entity_path + '/' + anim_state
                
                if anim_state == 'config.json':
                    continue
                
                if os.path.isdir(anim_path):
                    if anim_state not in config['animations']:
                        generate_config = True
                        config['animations'][anim_state] = {}
                        config['animations'][anim_state]['type'] = anim_state
                        config['animations'][anim_state]["frames"] = [5] * len(os.listdir(anim_path))
                        config['animations'][anim_state]["loop"] = False
                        config['animations'][anim_state]["speed"] = 1.0
                        config['animations'][anim_state]["offset"] = [0, 0]
                        config['animations'][anim_state]["outline"] = None

            if generate_config:
                save_json(f'{ANIMATIONS_PATH}{entity_id}/config.json', config)
                
    def new(self, anim_id):
        return self.animations[anim_id].copy() if anim_id in self.animations else None