import pygame

from .utils import load_json, save_json, load_dir_list

TILE_PATH = 'data/images/tiles/'

TILE_EXTRACTS = {
    'destructables': ['decor', (0, 1)],
    'trees': ['foliage', (0, 1)],
    'grass': ['grass', (0,)]
}

class Tilemap:
    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size
        self.tiles = load_dir_list(TILE_PATH, colorkey=(0, 0, 0))
        
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
            if str_loc in self.tilemap:
                rects.append(pygame.Rect(tile_loc[0] * self.tile_size, tile_loc[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    # gets position in tiles
    def get_tile(self, pos):
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        str_pos = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if str_pos in self.tilemap:
            return True
        
        
    def tile_collide(self, pos):
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap:
            return True
    
    def extract(self, extract_type, keep=True, offgrid=True):
        extract_list = []
        if offgrid:
            for layer in self.offgrid_tiles:
                for tile in self.offgrid_tiles[layer].copy():
                    if extract_type in TILE_EXTRACTS:
                        extract_id_pair = TILE_EXTRACTS[extract_type]
                        if tile['type'] in extract_id_pair[0] and tile['variant'] in extract_id_pair[1]:
                            extract_list.append(tile)
                            if not keep:
                                self.offgrid_tiles[layer].remove(tile)
        else:
            pass 
                    
        return extract_list

    def load_destructables(self, em):
        for crate in self.extract('destructables', keep=False):
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
            
    
    # gives grid positions (USES GRID POS)
    def remove_tile(self, tile_data):
        tile_pos = tile_data['tile_pos']
        layer = tile_data['layer']
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc][layer] in self.tilemap:
                self.tilemap[tile_loc][layer] = {}

    
    def add_offgrid_tile(self, tile_data):   
        layer = tile_data['layer']
        if layer in self.offgrid_tiles:
            self.offgrid_tiles[layer].append(tile_data)
        else:
            self.offgrid_tiles[layer] = []
            self.offgrid_tiles[layer].append(tile_data)
            
    def remove_offgrid_tile(self, layer, curr_mpos=(0,0)):
        if layer in self.offgrid_tiles:
            for tile_data in self.offgrid_tiles[layer]:
                tile_r = pygame.Rect(*tile_data['pos'], self.tile_size, self.tile_size)
                if tile_r.collidepoint(curr_mpos):
                    self.offgrid_tiles[layer].remove(tile_data)
                
    # be careful of layer in self.tilemap because when converted from json the layer is in STRING          
    def render(self, surf, offset=(0, 0)):
        for layer in self.offgrid_tiles: 
            tile_layer = self.offgrid_tiles[layer]
            for tile in tile_layer:
                surf.blit(self.tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                
        for y in range(self.game.world.camera.pos[1] // self.tile_size, ((self.game.world.camera.pos[1] + surf.get_height()) // self.tile_size) + 1):
            for x in range(self.game.world.camera.pos[0] // self.tile_size, ((self.game.world.camera.pos[0] + surf.get_width()) // self.tile_size) + 1):
                tile_loc = str(x) + ';' + str(y)
                if tile_loc in self.tilemap:
                    for tile_data in sorted(int(layer) for layer in self.tilemap[tile_loc]):
                        tile = self.tilemap[tile_loc][str(tile_data)]
                        surf.blit(self.tiles[tile['type']][tile['variant']], (tile['tile_pos'][0] * self.tile_size - offset[0], tile['tile_pos'][1] * self.tile_size - offset[1]))
                                
                        
                        
        
                    
                    