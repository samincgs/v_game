import pygame
import os

from .config import config
from .utils import load_image
from .animation_manager import AnimationManager

BASE_PATH = 'data/images/'  

class AssetManager:
    def __init__(self):
        self.animations = AnimationManager()
        self.misc = self.load_dir('misc')
        self.tiles = self.load_dir_list('tiles')
    
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
        
        