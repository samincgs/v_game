# import os

# from .config import config
# from .utils import load_imgs

# ANIMATIONS_PATH = 'data/images/animations/'
# COLORKEY = (0, 0, 0)

# class Animation:
#     def __init__(self, anim_id, images):
#         self.id = anim_id
#         self.images = images
#         self.config = config['animations'][self.id]
#         self.frame = 0
#         self.frame_index = 0
                
#     @property
#     def img(self):
#         return self.images[self.frame_index]
    
#     @property
#     def duration(self):
#         return sum(self.config['frames'])
    
#     def copy(self):
#         return Animation(self.id, self.images)
        
#     def play(self, dt):
#         self.frame += dt * 60 * self.config['speed']
        
#         if self.config['loop']:
#             if self.frame > self.duration:
#                 self.frame -= self.duration
        
#         self.frame_index = int(self.frame / self.duration * len(self.config['frames']))
#         self.frame_index = min(self.frame_index, len(self.config['frames']) - 1)
        
# class AnimationManager:
#     def __init__(self):
#         self.animations = {}
        
#         for anim_id in os.listdir(ANIMATIONS_PATH):
#             images = load_imgs(path=ANIMATIONS_PATH + '/' + anim_id, colorkey=COLORKEY)
#             self.animations[anim_id] = Animation(anim_id, images)
                                   
#     def new(self, anim_id):
#         return self.animations[anim_id].copy()