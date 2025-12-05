import scripts.pgtools as pt

BASE_PATH = 'data/images/' 
BASE_PATH_FONT = 'data/fonts/' 
FONTS = {
    "small_white": [BASE_PATH_FONT + 'main_font.png', (255, 255, 255)],
    "small_black": [BASE_PATH_FONT + 'main_font.png', (0, 0, 1)],
    "small_red": [BASE_PATH_FONT + 'main_font.png', (203, 10, 7)],
}

class Assets:
    def __init__(self):
        self.animations = pt.AnimationManager()
        self.misc = pt.utils.load_imgs_dict(BASE_PATH + 'misc')
        self.weapons = pt.utils.load_imgs_dict(BASE_PATH + 'weapons')
        self.particles = pt.utils.load_directory(BASE_PATH + 'particles')
        
        self.fonts = {font_name: pt.Font(font[0], font[1]) for font_name, font in FONTS.items()}
    
    
        
        