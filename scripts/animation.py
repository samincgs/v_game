import os

from .config import config
from .utils import load_image

ANIMATION_PATH = 'data/images/animations'
COLORKEY = (0, 0, 0)

class AnimationData:
    def __init__(self, path, colorkey=None):
        self.id = path.split('/')[-1]
        self.config = config['animations'][self.id]
        self.images = []
        for img in sorted(os.listdir(path)):
            self.images.append(load_image(path + '/' + img, colorkey))
        
    @property
    def duration(self):
        return sum(self.config['frames'])
    
class Animation:
    def __init__(self, animation_data):
        self.data = animation_data
        self.frame = 0
        self.frame_index = 0
    
    @property
    def img(self):
        return self.data.images[self.frame_index]
    
    def play(self, dt):
        self.frame += dt * 60 * self.data.config['speed']
        
        if self.data.config['loop']:
            if self.frame > self.data.duration:
                self.frame -= self.data.duration
        
        self.frame_index = int(self.frame / self.data.duration * len(self.data.config['frames']))
        self.frame_index = min(self.frame_index, len(self.data.config['frames']) - 1)
        
class AnimationManager:
    def __init__(self):
        self.animations = {}
        for anim in os.listdir(ANIMATION_PATH):
            self.animations[anim] = AnimationData(ANIMATION_PATH + '/' + anim, COLORKEY)
                    
    def new(self, anim_id):
        return Animation(self.animations[anim_id])