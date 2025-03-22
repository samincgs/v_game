import pygame
import os

from .utils import load_img, load_json, save_json, load_dir_list, clip

TILE_PATH = 'data/images/tiles/'

class Tilemap:
    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        
        self.tilemap = {} # { {'5;7' : 0 {{'type': 'grass', 'variant': 0, 'pos': [x, x]}}}}
        self.offgrid_tiles = {} # {0: [{'type': 'grass', 'variant': 0, 'pos': [x, x]}]}
        
    def collision_test(self, obj, obj_list):
        collision_list = []
        for rect in obj_list:
            if obj.colliderect(rect):
                collision_list.append(rect)
        return collision_list
    
    def get_nearby_rects(self, pos):
        rects = []
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        check_locs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        for loc in check_locs:
            tile_loc = (tile_pos[0] + loc[0], tile_pos[1] + loc[1])
            str_loc = str(tile_loc[0]) + ';' + str(tile_loc[1])
            if str_loc in self.tilemap and self.tilemap[str_loc]:
                rects.append(pygame.Rect(tile_loc[0] * self.tile_size, tile_loc[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    # gets position in tiles
    def get_tile(self, pos):
        str_pos = str(pos[0]) + ';' + str(pos[1])
        if str_pos in self.tilemap:
            return True
        return False
        
    def tile_collide(self, pos):
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap and self.tilemap[tile_loc]:
            return True
    
    def extract(self, id_pairs, keep=True, offgrid=True): # id_pairs -> ('decor', (1, 2)) tile type, tile variants
        extract_list = []
        if offgrid:
            for layer in self.offgrid_tiles:
                for tile in self.offgrid_tiles[layer].copy():
                    if tile['type'] in id_pairs[0] and tile['variant'] in id_pairs[1]:
                        extract_list.append(tile)
                        if not keep:
                            self.offgrid_tiles[layer].remove(tile)
        else:
            pass
        
        return extract_list
                    
        
    # additional
    def load_destructables(self, em):
        for crate in self.extract(['decor', (0, 1)], keep=False):
            em.load_destructable(crate)
    
    def load_map(self, path):
        map_data = load_json(path)
        
        self.tilemap = map_data['tilemap'] 
        self.offgrid_tiles = map_data['offgrid_tiles']
    
    def write_map(self, path):
        map_data = {
            'tilemap': self.tilemap,
            'offgrid_tiles': self.offgrid_tiles,
            'tile_size': self.tile_size
        }
        
        save_json(path, data=map_data)
    
    # gives grid positions (USES GRID POS)
    def add_tile(self, tile_data):
        tile_pos = tile_data['tile_pos']
        layer = tile_data['layer']
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap:
            self.tilemap[tile_loc][layer] = tile_data
        else:
            self.tilemap[tile_loc] = {}
            self.tilemap[tile_loc][layer] = tile_data
            
    # gives grid positions (USES GRID POS)
    def remove_tile(self, tile_data):
        tile_pos = tile_data['tile_pos']
        layer = tile_data['layer']
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap:
            if layer in self.tilemap[tile_loc]:
                del self.tilemap[tile_loc][layer]
    
    def add_offgrid_tile(self, tile_data):   
        layer = tile_data['layer']
        if layer in self.offgrid_tiles:
            self.offgrid_tiles[layer].append(tile_data)
        else:
            self.offgrid_tiles[layer] = []
            self.offgrid_tiles[layer].append(tile_data)
            
    def remove_offgrid_tile(self, layer, curr_mpos=(0,0)):
        layer = layer
        if layer in self.offgrid_tiles:
            for tile_data in self.offgrid_tiles[layer]:
                tile_r = pygame.Rect(*tile_data['pos'], self.tile_size, self.tile_size)
                if tile_r.collidepoint(curr_mpos):
                    self.offgrid_tiles[layer].remove(tile_data)
                
    def render_visible(self, surf, offset=(0, 0)):
        tiles = self.load_spritesheets('data/images/spritesheets/')
        render_queue = []
        
        for layer in sorted(int(layer) for layer in self.offgrid_tiles): 
            tile_layer = self.offgrid_tiles[str(layer)]
            for tile in tile_layer:
                render_queue.append((int(layer), tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
                # surf.blit(tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                
        for x in range(offset[0] // self.tile_size, ((offset[0] + surf.get_width()) // self.tile_size) + 1):
            for y in range(offset[1] // self.tile_size, ((offset[1] + surf.get_height()) // self.tile_size) + 1):
                tile_loc = str(x) + ';' + str(y)
                if tile_loc in self.tilemap:
                    for layer in sorted(int(layer) for layer in self.tilemap[tile_loc]):
                        tile = self.tilemap[tile_loc][str(layer)]
                        render_queue.append((int(layer), tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1])))
                        # surf.blit(tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1]))
                        
        render_queue.sort(key=lambda x: x[0]) # sort the layer
        
        for tile in render_queue:
            surf.blit(tile[1], tile[2])
        
                        
    def render_all(self, surf, offset=(0, 0)):
        tiles = self.load_spritesheets('data/images/spritesheets/')
        render_queue = []
        
        for layer in sorted(int(layer) for layer in self.offgrid_tiles): 
            tile_layer = self.offgrid_tiles[str(layer)]
            for tile in tile_layer:
                render_queue.append((int(layer), tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
                # surf.blit(tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                
        for loc in self.tilemap:
            for layer in sorted(int(layer) for layer in self.tilemap[loc]):
                tile = self.tilemap[loc][str(layer)]
                render_queue.append((int(layer), tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1])))
                # surf.blit(tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1]))
                
        render_queue.sort(key=lambda x: x[0]) # sort the layer
        
        for tile in render_queue:
            surf.blit(tile[1], tile[2])
                                
    def load_spritesheets(self, path):
        """Loads all spritesheets in a directory and extracts sprites."""
        
        spritesheet_dict = {}
        
        for img_file in os.listdir(path):
            if img_file.endswith('.png'): 
                tile_name = img_file.split('.')[0]  
                spritesheet_dict[tile_name] = []
                
                spritesheet = load_img(os.path.join(path, img_file))
                
                y = 1
                start_x = 1  
                
                while y < spritesheet.get_height():
                    tile_end = None
                    end_x = None
                    
                    for y2 in range(y, spritesheet.get_height()):
                        if spritesheet.get_at((start_x, y2))[:3] == (255, 0, 255): # MAGENTA
                            tile_end = y2 - 1
                            break
                    
                    for x2 in range(start_x, spritesheet.get_width()):
                        if spritesheet.get_at((x2, y))[:3] == (255, 0, 255): # MAGENTA
                            end_x = x2 - 1
                            break
                        
                    
                    if tile_end is not None and end_x is not None:
                        width, height = end_x - start_x + 1, tile_end - y + 1
                        img = clip(spritesheet, (start_x, y), (width, height))

                        spritesheet_dict[tile_name].append(img)

                        y = tile_end + 3 

                    else:
                        y = spritesheet.get_height() + 100  
                
        return spritesheet_dict
                            
        
                    
                    