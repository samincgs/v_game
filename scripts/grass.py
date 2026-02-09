import pygame
import math
import random

from scripts.pgtools.utils import load_imgs_list

GRASS_PATH = 'data/images/grass'
MAX_SWAY = 70


class GrassManager:
    def __init__(self, tile_size=16, grass_path=GRASS_PATH):
        self.tile_size = tile_size
        self.grass_assets = load_imgs_list(grass_path)
        self.grass = {}
        
    def place_grass(self, tile_pos, grass_variants, quantity, y_range):
        grass_id = tuple(tile_pos)
        if grass_id not in self.grass:
            self.grass[grass_id] = GrassTile(self.tile_size, tile_pos, self.grass_assets, grass_variants, quantity, y_range)
            
    def update_render(self, surf, visible_range, offset=(0, 0), master_clock=0):            
        for y in visible_range[1]:
            for x in visible_range[0]:
                tile_loc = (x, y)
                if tile_loc in self.grass:
                    self.grass[tile_loc].update(master_clock)
                    self.grass[tile_loc].render(surf, offset=offset)


class GrassTile:
    def __init__(self, tile_size, tile_pos, grass_assets, grass_variants, quantity, padding_range):
        self.tile_size = tile_size
        self.tile_pos = list(tile_pos)
        self.grass_assets = grass_assets
        self.grass_variants = grass_variants
        self.padding_range = padding_range
        
        self.blades = []
        
        for _ in range(quantity):
            img = self.grass_assets[random.choice(self.grass_variants)]
            x_offset = random.uniform(-tile_size / 2, tile_size / 2)
            y_offset = random.uniform(padding_range[0], padding_range[1])
            self.blades.append(GrassBlade(tile_size, img, x_offset, y_offset))
            
    
    def update(self, master_clock=0):
        for blade in self.blades:
            blade.update(master_clock)
    
    def render(self, surf, offset=(0, 0)):
        render_pos = (self.tile_pos[0] * self.tile_size - offset[0], self.tile_pos[1] * self.tile_size - offset[1])
        
        for blade in self.blades:
            blade.render(surf, render_pos)


class GrassBlade:
    def __init__(self, tile_size, img, x_offset, y_offset):
        self.tile_size = tile_size
        self.img = img
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.rotation = 0
        
    def update(self, master_clock=0):
        pass
        
    def render(self, surf, location):
        img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(img, (location[0] - img.get_width() / 2 + self.tile_size / 2 + self.x_offset, location[1] - img.get_height() / 2 + self.tile_size + self.y_offset))