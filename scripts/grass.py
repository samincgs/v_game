import pygame
import math
import random

from scripts.pgtools.utils import load_imgs_list

GRASS_PATH = 'data/images/grass'

class GrassManager:
    def __init__(self, tile_size=16, grass_path=GRASS_PATH):
        self.tile_size = tile_size
        self.grass_assets = load_imgs_list(grass_path)
        self.grass = {}
        
    def place_grass(self, tile_pos, grass_variants, quantity):
        grass_id = tuple(tile_pos)
        if grass_id not in self.grass:
            self.grass[grass_id] = GrassTile(self.tile_size, tile_pos, self.grass_assets, grass_variants, quantity)
            
    def update(self, master_clock=0):
        for grass in self.grass:
            self.grass[grass].update(master_clock)
            
    def render(self, surf, visible_range, offset=(0, 0), y_padding=2):        
        for y in visible_range[1]:
            for x in visible_range[0]:
                tile_loc = (x, y)
                if tile_loc in self.grass:
                    self.grass[tile_loc].render(surf, offset=offset, y_padding=y_padding)
        
            
class GrassTile:
    def __init__(self, tile_size, tile_pos, grass_assets, grass_variants, quantity):
        self.tile_size = tile_size
        self.tile_pos = list(tile_pos)
        self.grass_assets = grass_assets
        self.grass_variants = grass_variants
        
        self.blades = []
        
        for i in range(quantity):
            img = self.grass_assets[random.choice(self.grass_variants)]
            self.blades.append(GrassBlade(tile_size, img))
            
    
    def update(self, master_clock=0):
        for blade in self.blades:
            blade.update(master_clock)
    
    def render(self, surf, offset=(0, 0), y_padding=2):
        render_pos = (self.tile_pos[0] * self.tile_size - offset[0], self.tile_pos[1] * self.tile_size - offset[1] + y_padding)
        
        for blade in self.blades:
            blade.render(surf, render_pos, offset=offset)


class GrassBlade:
    def __init__(self, tile_size, img):
        self.tile_size = tile_size
        self.img = img
        self.rotation = 0
        
    def update(self, master_clock=0):
        self.rotation += math.sin(master_clock / 4) * 3
        
    def render(self, surf, location, offset=(0, 0)):
        img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(img, (location[0] - img.get_width() / 2 + self.tile_size / 2, location[1] - img.get_height() / 2 + self.tile_size))