import os

from .animation import AnimationManager
from .font import Font
from .utils import load_dir, load_dir_list


BASE_PATH = 'data/images/' 
BASE_PATH_FONT = 'data/fonts/' 


FONTS = {
    "small_white": [BASE_PATH_FONT + 'main_font.png', (255, 255, 255)],
    "small_black": [BASE_PATH_FONT + 'main_font.png', (0, 0, 1)],
    "small_red": [BASE_PATH_FONT + 'main_font.png', (203, 10, 7)],
    # "large_white": (BASE_PATH_FONT + 'large_font.png', (255, 255, 255)),
    # "large_black": (BASE_PATH_FONT + 'large_font.png', (0, 0, 1)),
}
class Assets:
    def __init__(self):
        self.animations = AnimationManager()
        self.misc = load_dir(BASE_PATH + 'misc')
        self.weapons = load_dir(BASE_PATH + 'weapons')
        self.particles = load_dir_list(BASE_PATH + 'particles')
        # self.items = self.load_dir('items')
        
        self.fonts = {font_name: Font(font[0], font[1]) for font_name, font in FONTS.items()}
    
    
        
        