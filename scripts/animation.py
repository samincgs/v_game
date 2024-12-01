import os

from .config import config
from .utils import load_image

ANIMATION_PATH = 'data/images/animations'
COLORKEY = (0, 0, 0)

class AnimationData:
    def __init__(self, path, colorkey=None):
        self.id = path.split('/')[-1]
        self.images = []
        for img in sorted(os.listdir(path)):
            self.images.append(load_image(path + '/' + img, colorkey))
        
        self.config = config['animations'][self.id]
        
    @property
    def duration(self):
        return sum(self.config['frames'])
    
    
class Animation:
    def __init__(self, animation_data):
        self.data = animation_data
        self.frame = 0
        self.img = animation_data.images[0]
    
    def play(self, dt):
        self.frame += dt * 60 * self.data.config['speed']
        
        if self.data.config['loop']:
            if self.frame > self.data.duration:
                self.frame -= self.data.duration
        
        frame_index = int(self.frame / self.data.duration * len(self.data.config['frames']))
        frame_index = min(frame_index, len(self.data.config['frames']) - 1)
        self.img = self.data.images[frame_index]
        
        
class AnimationManager:
    def __init__(self):
        self.animations = {}
        for anim in os.listdir(ANIMATION_PATH):
            self.animations[anim] = AnimationData(ANIMATION_PATH + '/' + anim, COLORKEY)
                    
    def new(self, anim_id):
        return Animation(self.animations[anim_id])