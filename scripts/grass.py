import pygame
import math
import random

from scripts.pgtools.utils import load_imgs_list, get_distance

GRASS_PATH = 'data/images/grass'
MAX_BEND = 70
FORCE_AMOUNT = 90
DAMPING = 0.92

class GrassManager:
    def __init__(self, tile_size=16, grass_path=GRASS_PATH):
        self.tile_size = tile_size
        self.grass_assets = load_imgs_list(grass_path)
        self.grass = {}
    
    def place_grass(self, tile_pos, grass_variants, quantity, vertical_range):
        grass_id = tuple(tile_pos)
        if grass_id not in self.grass:
            self.grass[grass_id] = GrassTile(self.tile_size, tile_pos, self.grass_assets, grass_variants, quantity, vertical_range)
    
    def apply_bend(self, pos, radius=8, dropoff=12):
        entity_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tile_radius = math.ceil((radius + dropoff) / self.tile_size)
        
        for tx in range(entity_pos[0] - tile_radius, entity_pos[0] + tile_radius):
            for ty in range(entity_pos[1] - tile_radius, entity_pos[1] + tile_radius):
                tile_pos = (tx, ty)
                if tile_pos in self.grass:
                    grass_tile = self.grass[tile_pos]
                    for blade in grass_tile.blades:
                        blade.bend(pos, radius, dropoff)

                
    def update_render(self, game, surf, visible_range, offset=(0, 0), master_clock=0, rot_func=None):            
        for y in visible_range[1]:
            for x in visible_range[0]:
                tile_loc = (x, y)
                if tile_loc in self.grass:
                    grass = self.grass[tile_loc]
                    if not game.window.pause_state:
                        grass.update(master_clock, rot_func)
                    grass.render(surf, offset=offset)

class GrassTile:
    def __init__(self, tile_size, tile_pos, grass_assets, grass_variants, quantity, vertical_range):
        self.tile_size = tile_size
        self.tile_pos = list(tile_pos)
        self.grass_assets = grass_assets
        self.grass_variants = grass_variants
        self.vertical_range = vertical_range
        
        self.blades = []
        
        for _ in range(quantity):
            img = self.grass_assets[random.choice(self.grass_variants)]
            horizontal_offset = random.uniform(-tile_size / 2 + 1, tile_size / 2 - 1)
            vertical_offset = random.uniform(vertical_range[0], vertical_range[1])
            self.blades.append(GrassBlade(tile_size, tile_pos, img, horizontal_offset, vertical_offset))
            
    
    def update(self, master_clock=0, rot_func=None):
        for blade in self.blades:
            blade.update(master_clock, rot_func)
    
    def render(self, surf, offset=(0, 0)):
        for blade in self.blades:
            blade.render(surf, offset=offset)

class GrassBlade:
    def __init__(self, tile_size, tile_pos, img, horizontal_offset, vertical_offset):
        self.tile_size = tile_size
        self.tile_pos = list(tile_pos)
        self.img = img
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset
        
        self.rotation = 0
        self.bend_rotation = 0
        
    @property
    def render_pos(self):
        return (self.tile_pos[0] * self.tile_size + self.tile_size / 2 + self.horizontal_offset, self.tile_pos[1] * self.tile_size + self.tile_size + 1 + self.vertical_offset)
    
    def bend(self, force_point, force_radius, force_dropoff):
        blade_loc = self.render_pos

        dis = get_distance(force_point, blade_loc)

        if dis < force_radius:
            force = 2
        else:
            force = 1 - min(max(0, dis - force_radius) / force_dropoff, 1)

        if force <= 0:
            return

        direction = 1 if force_point[0] > blade_loc[0] else -1

        self.bend_rotation = direction * force * FORCE_AMOUNT
        self.bend_rotation = max(-MAX_BEND, min(MAX_BEND, self.bend_rotation))
        
    
    def update(self, master_clock=0, rot_func=None):
        sway_rotation = math.sin(self.tile_pos[0] / 120 + master_clock * 2.7) * 10
        if rot_func:
            sway_rotation = rot_func(self.tile_pos)
        
        self.bend_rotation *= DAMPING
    
        self.rotation = sway_rotation + self.bend_rotation
        

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(img, (self.render_pos[0] - offset[0] - img.get_width() / 2, self.render_pos[1] - offset[1] - img.get_height() / 2))