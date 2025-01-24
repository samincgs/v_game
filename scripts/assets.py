import os

from . import animation
from .font import Font
from .utils import load_image


BASE_PATH = 'data/images/' 
BASE_PATH_FONT = 'data/fonts/' 

FONTS = {
    "small_white": [BASE_PATH_FONT + 'small_font.png', (255, 255, 255)],
    "small_black": [BASE_PATH_FONT + 'small_font.png', (0, 0, 1)],
    "small_red": [BASE_PATH_FONT + 'small_font.png', (203, 10, 7)],
    # "large_white": (BASE_PATH_FONT + 'large_font.png', (255, 255, 255)),
    # "large_black": (BASE_PATH_FONT + 'large_font.png', (0, 0, 1)),
}
class Assets:
    def __init__(self):
        self.animations = animation.AnimationManager()
        self.misc = self.load_dir('misc')
        self.weapons = self.load_dir('weapons')
        self.particles = self.load_dir_list('particles')
        self.tiles = self.load_dir_list('tiles')
        # self.items = self.load_dir('items')
        
        self.fonts = {font_name: Font(font[0], font[1]) for font_name, font in FONTS.items()}
    
    def load_dir(self, path):
        image_dir = {}
        for img in os.listdir(BASE_PATH + path):
            image_dir[img.split('.')[0]] = load_image(BASE_PATH + path + '/' + img)
        return image_dir
    
    def load_dir_list(self, path):
        image_dir = {}
        for folder in os.listdir(BASE_PATH + path):
            image_dir[folder] = []
            for img in os.listdir(BASE_PATH + path + '/' + folder):
                image_dir[folder].append(load_image(os.path.join(BASE_PATH, path, folder, img)))                                       
        return image_dir
        
        