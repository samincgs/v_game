import os

from .font import Font
from .config import config
from .utils import load_image
from .animation import AnimationManager

BASE_PATH = 'data/images/' 
BASE_PATH_FONT = 'data/fonts/' 

FONTS = {
    "small_white": (BASE_PATH_FONT + 'small_font.png', (255, 255, 255)),
    "small_black": (BASE_PATH_FONT + 'small_font.png', (0, 0, 1)),
    "large_white": (BASE_PATH_FONT + 'large_font.png', (255, 255, 255)),
    "large_black": (BASE_PATH_FONT + 'large_font.png', (0, 0, 1)),
}

class Asset:
    def __init__(self):
        self.animations = AnimationManager()
        self.misc = self.load_dir('misc')
        self.weapons = self.load_dir('weapons')
        self.particles = self.load_dir_list('particles')
        self.tiles = self.load_dir_list('tiles')
        self.items = self.load_dir('items')
        
        self.fonts = {font_name: Font(font[0], font[1]) for font_name, font in FONTS.items()}
    
    def load_dir(self, path):
        image_dir = {}
        for img in os.listdir(BASE_PATH + path):
            image_dir[img.split('.')[0]] = load_image(BASE_PATH + path + '/' + img)
        return image_dir
    
    def load_dir_list(self, path):
        image_dir = {}
        for root, dirs, files in os.walk(BASE_PATH + path):
            if files:
                key = root.split('\\')[1]
                image_dir[key] = []
                for file in files:
                    img_path = root.replace('\\', '/') + '/' + str(file)
                    img = load_image(img_path)
                    image_dir[key].append(img)
                                        
        return image_dir
        
        