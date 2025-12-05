import os
import pygame
from .utils import load_json, save_json, load_img, clip

SPRITESHEET_PATH = 'data/images/spritesheets/'
TILES_AROUND = [(0, 0), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1), (0, 1), (1, 1), (-1, 1)]
OFFSET_N4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
OFFSET_N8 = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
AUTOTILE_BORDERS = {
    0: [(0, 1), (1, 0)],
    1: [(-1, 0), (0, 1), (1, 0)],
    2: [(-1, 0), (0, 1)],
    3: [(-1, 0), (0, -1), (0, 1)],
    4: [(-1, 0), (0, -1)],
    5: [(-1, 0), (0, -1), (1, 0)],
    6: [(0, -1), (1, 0)],
    7: [(0, -1), (0, 1), (1, 0)],
    8: [(-1, 0), (0, -1), (0, 1), (1, 0)]
}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        
        self.tilemap = {} # { {'5;7' : 0 {{'type': 'grass', 'variant': 0, 'pos': [x, x]}}}}
        self.offgrid_tiles = {} # {0: [{'type': 'grass', 'variant': 0, 'pos': [x, x]}]}
        self.tiles = self.load_spritesheets(SPRITESHEET_PATH)
        self.tiles_config = self.load_config()
        
        self.physics_tiles = list(self.tiles_config)
        self.autotile_types = list(self.tiles_config)
        
    def get_nearby_rects(self, pos):
        rects = []
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for loc in TILES_AROUND:
            tile_loc = (tile_pos[0] + loc[0], tile_pos[1] + loc[1])
            str_loc = str(tile_loc[0]) + ';' + str(tile_loc[1])
            if str_loc in self.tilemap:
                for layer in self.tilemap[str_loc]:
                    tile_type = self.tilemap[str_loc][layer]['type']
                    tile_variant = self.tilemap[str_loc][layer]['variant']
                    if tile_type in self.physics_tiles:
                        tile_offset = (0, 0)
                        if tile_type in self.tiles_config:
                            tile_offset = self.tiles_config[tile_type]['tile_offsets'][str(tile_variant)]
                        rects.append(pygame.Rect(tile_loc[0] * self.tile_size + tile_offset[0], tile_loc[1] * self.tile_size + tile_offset[1], self.tile_size - tile_offset[0], self.tile_size - tile_offset[1]))         
        return rects

    # left, right, top, bottom
    def get_map_edges(self):
        edges = [99999, -99999, 99999, -99999]
        for pos in self.tilemap:
            x, y = int(pos.split(';')[0]) * self.tile_size, int(pos.split(';')[1]) * self.tile_size
            if x < edges[0]:
                edges[0] = x
            if x > edges[1]:
                edges[1] = x + self.tile_size
            if y < edges[2]:
                edges[2] = y
            if y > edges[3]:
                edges[3] = y + self.tile_size
        return edges        
        
    # gets position in tiles
    def get_tile(self, pos):
        str_pos = str(pos[0]) + ';' + str(pos[1])
        if str_pos in self.tilemap:
            return True
        return False
    
    # gets position in tiles
    def get_tile_by_layer(self, pos, layer):
        str_pos = str(pos[0]) + ';' + str(pos[1])
        if str_pos in self.tilemap and layer in self.tilemap[str_pos]:
            return True
        return False
        
    def tile_collide(self, pos):
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap:
            return True
    
    # make better later
    def extract(self, id_pairs, keep=False, offgrid=True):
        extract_list = []
        if offgrid:
            for layer in self.offgrid_tiles:
                for tile in self.offgrid_tiles[layer].copy():
                    if tile['type'] == id_pairs[0] and tile['variant'] in id_pairs[1]:
                        extract_list.append(tile)
                        if not keep:
                            self.offgrid_tiles[layer].remove(tile)
        else:
            for loc in self.tilemap.copy():
                for layer in self.tilemap[loc].copy():
                    tile = self.tilemap[loc][layer]
                    if tile['type'] == id_pairs[0] and tile['variant'] in id_pairs[1]:
                        extract_list.append(tile)
                        if not keep:
                            self.remove_tile(tile)
        
        return extract_list
            
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
            # delete tile loc if there is no tile data so it doesnt leave a random empty dict
            if not len(self.tilemap[tile_loc]):
                del self.tilemap[tile_loc]
        
    
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
    
    def set_physics_tiles(self, physics_tiles):
        self.physics_tiles = physics_tiles
        
    def set_autotile_types(self, autotile_types):
        self.autotile_types = autotile_types
    
    def autotile(self, selection_rect, current_layer): # keybinding: t
        if selection_rect: # only with rect
            for loc in self.tilemap:
                for layer in (int(layer) for layer in self.tilemap[loc]):
                    layer = str(layer)
                    if current_layer == layer:
                        layer = str(layer)
                        tile = self.tilemap[loc][layer]
                        neighbours = []
                        for offset in OFFSET_N4:
                            tile_loc = (tile['tile_pos'][0] + offset[0], tile['tile_pos'][1] + offset[1])
                            if not selection_rect.collidepoint((tile_loc[0] * self.tile_size, tile_loc[1] * self.tile_size)):  # only with rect
                                continue  
                            str_loc = str(tile_loc[0]) + ';' + str(tile_loc[1])
                            if str_loc in self.tilemap:
                                if layer in self.tilemap[str_loc]:
                                    if tile['type'] == self.tilemap[str_loc][layer]['type'] and tile['type'] in self.autotile_types:
                                        neighbours.append(offset)
                        neighbours = sorted(neighbours)
                        for border in AUTOTILE_BORDERS:
                            border_list = sorted(AUTOTILE_BORDERS[border])
                            if neighbours == border_list:
                                tile['variant'] = border
    
    
    def floodfill(self, curr_pos, tile_data, offset=(0, 0)):
        floodfill_list = [curr_pos]
        visited = set()
        
        MAX_TILES = 200
        
        while floodfill_list:            
            tile = floodfill_list.pop(0)
            
            if tuple(tile) in visited:
                continue
            
            visited.add(tuple(tile))
            
            if len(floodfill_list) > MAX_TILES:
                return
                
            scaled_mpos = (tile[0] + offset[0] * self.tile_size, tile[1] + offset[1] * self.tile_size)
            tile_data = {'type': tile_data['type'], 'variant': tile_data['variant'], 'pos': scaled_mpos, 'tile_pos': tuple(tile), 'layer': tile_data['layer']}
            self.add_tile(tile_data)
            
            bordering_tiles = [[tile[0] + 1, tile[1]], [tile[0] - 1, tile[1]], [tile[0], tile[1] + 1], [tile[0], tile[1] - 1]]
            for b in bordering_tiles:
                if not self.get_tile_by_layer(b, tile_data['layer']) and tuple(b) not in visited:
                    floodfill_list.append(b)
                    
    
    def load_spritesheets(self, path): # loads all spritesheets in a directory and extracts sprites

        CYAN = (0, 255, 255)
        MAGENTA = (255, 0, 255)
        
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
                        if spritesheet.get_at((start_x, y2))[:3] in {MAGENTA, CYAN}: # MAGENT, CYAN
                            tile_end = y2 - 1
                            break
                    for x2 in range(start_x, spritesheet.get_width()):
                        if spritesheet.get_at((x2, y))[:3] in {MAGENTA, CYAN}: # MAGENTA or CYAN
                            end_x = x2 - 1
                            break
                    if tile_end is not None and end_x is not None:
                        width, height = end_x - start_x + 1, tile_end - y + 1
                        img = clip(spritesheet, (start_x, y), (width, height))
                        spritesheet_dict[tile_name].append(img)
                        y = tile_end + 3 
                    else:
                        y += 1
                        
                if spritesheet.get_at((0, 0)) == CYAN:
                    if tile_name + '.json' not in os.listdir(path):
                        tile_variants = len(spritesheet_dict[tile_name])
                        data = {'tile_offsets': {}}
                        for i in range(tile_variants):
                            data['tile_offsets'][i] = [0, 0]
                        save_json(path + tile_name + '.json', data)
                                         
        return spritesheet_dict
    
    
    def load_config(self):
        tileset_config = {}
        for tile_json in os.listdir(SPRITESHEET_PATH):
            name, ext = tile_json.split('.')
            if ext == 'json':
                tileset_config[name] = load_json(SPRITESHEET_PATH + tile_json)
        return tileset_config
    
    def render_visible(self, surf, visible_range=(0, 0), offset=(0, 0)):
        render_queue = []
        
        for layer in sorted(int(layer) for layer in self.offgrid_tiles): 
            tile_layer = self.offgrid_tiles[str(layer)]
            for tile in tile_layer:
                render_queue.append((int(layer), self.tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
        
        for y in range(visible_range[1]):
            for x in range(visible_range[0]):
                tile_loc = str(x) + ';' + str(y)
                if tile_loc in self.tilemap:
                    for layer in sorted(int(layer) for layer in self.tilemap[tile_loc]):
                        tile = self.tilemap[tile_loc][str(layer)]
                        render_queue.append((int(layer), self.tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1])))
                        
        render_queue.sort(key=lambda x: x[0]) # sort the layer
        
        for tile in render_queue:
            surf.blit(tile[1], (int(tile[2][0]), int(tile[2][1])))
 
                        
    def render_all(self, surf, offset=(0, 0)):
        render_queue = []
        
        for layer in sorted(int(layer) for layer in self.offgrid_tiles): 
            tile_layer = self.offgrid_tiles[str(layer)]
            for tile in tile_layer:
                render_queue.append((int(layer), self.tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
                
        for loc in self.tilemap:
            for layer in sorted(int(layer) for layer in self.tilemap[loc]):
                tile = self.tilemap[loc][str(layer)]
                render_queue.append((int(layer), self.tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1])))
                
        render_queue.sort(key=lambda x: x[0]) # sort the layer
        
        for tile in render_queue:
            surf.blit(tile[1], tile[2])
                                
    
                        
        
                    
                    