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
            
    def remove_offgrid_tile(self, layer, curr_mpos=(0,0)):
        if layer in self.offgrid_tiles:
            for tile_data in self.offgrid_tiles[layer]:
                print(tile_data)
                tile_r = pygame.Rect(*tile_data['pos'], self.tile_size, self.tile_size)
                if tile_r.collidepoint(curr_mpos):
                    print('collided')
                    self.offgrid_tiles[layer].remove(tile_data)
                
                
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
                
    def render_editor(self, curr_layer, layer_opacity, surf, offset=(0,0)):
        for layer in self.offgrid_tiles:
            tile_layer = self.offgrid_tiles[layer]
            for tile in tile_layer:
                if not layer_opacity:
                    img = self.game.assets.tiles[tile['type']][tile['variant']]
                    surf.blit(img, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                else:
                    if curr_layer == layer:
                        img = self.game.assets.tiles[tile['type']][tile['variant']]
                        surf.blit(img, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
                    else:
                        img = self.game.assets.tiles[tile['type']][tile['variant']].copy()
                        img.set_alpha(100)
                        surf.blit(img, (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for layer in self.tilemap: # 0
            tile_layer = self.tilemap[layer]
            for loc in sorted(tile_layer):
                tile = tile_layer[loc]
                if not layer_opacity:
                    img = self.game.assets.tiles[tile['type']][tile['variant']]
                    surf.blit(img, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                else:
                    if curr_layer == layer:
                        img = self.game.assets.tiles[tile['type']][tile['variant']]
                        surf.blit(img, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                    else:
                        img = self.game.assets.tiles[tile['type']][tile['variant']].copy()
                        img.set_alpha(100)
                        surf.blit(img, (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                    
                    