import pygame
import json
import math

class Tilemap:
    def __init__(self, game, tile_size, view_size):
        self.game = game
        self.tile_size = tile_size 
        self.view_size = view_size 
        
        self.tilemap = {} # { 0 : {'5;7' : {'type': 'grass', 'variant': 0, 'pos': [x, x]}}}
        self.offgrid_tiles = {} # {0: [{'type': 'grass', 'variant': 0, 'pos': [x, x]}]}
        
    def load_map(self, path):
        f = open(path, 'r')
        map_data = json.load(fp=f)
        f.close()
        
        self.tilemap = map_data['tilemap'] 
        self.offgrid_tiles = map_data['offgrid_tiles']
        
    def write_map(self, path):
        map_data = {
            'tilemap': self.tilemap,
            'offgrid_tiles': self.offgrid_tiles,
            'tile_size': self.tile_size
        }
        
        f = open(path, 'w')
        json.dump(map_data, fp=f)
        f.close()
    
    # gives grid positions (USES GRID POS)
    def add_tile(self, tile, layer):
            pos = tile['pos']
            if layer in self.tilemap:
                tile_loc = str(pos[0]) + ';' + str(pos[1])
                self.tilemap[layer][tile_loc] = tile
            else:
                self.tilemap[layer] = {} # if layer doesnt exist
    
    # gives grid positions (USES GRID POS)
    def remove_tile(self, tile, layer):
        pos = tile['pos']
        if layer in self.tilemap.copy():
            tile_loc = str(pos[0]) + ';' + str(pos[1])
            if tile_loc in self.tilemap[layer]:
                del self.tilemap[layer][tile_loc]

    def add_offgrid_tile(self, tile, layer):   
        if layer in self.offgrid_tiles:
            self.offgrid_tiles[layer].append(tile)
        else:
            self.offgrid_tiles[layer] = []
            self.offgrid_tiles[layer].append(tile)
            
    def remove_offgrid_tile(self, tile, layer):
        pass
                
                
        
        
    
    def render(self, surf, offset=(0, 0)):
        
        for layer in self.offgrid_tiles:
            tile_layer = self.offgrid_tiles[layer]
            for tile in tile_layer:
                surf.blit(self.game.assets.tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for layer in self.tilemap: # 0
            tile_layer = self.tilemap[layer]
            for loc in sorted(tile_layer):
                tile = tile_layer[loc]
                surf.blit(self.game.assets.tiles[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                
    def render_editor(self):
        pass
                    
                    