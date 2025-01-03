import pygame
import json

class Tilemap:
    def __init__(self, game, tile_size):
        self.game = game
        self.tile_size = tile_size 
        
        self.tilemap = {} # { 0 : {'5;7' : {'type': 'grass', 'variant': 0, 'pos': [x, x]}}}
        self.offgrid_tiles = {} # {0: [{'type': 'grass', 'variant': 0, 'pos': [x, x]}]}
        
        # self.non_collideables = {'grass'}
    
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
            for layer in sorted(self.tilemap):
                if str_loc in self.tilemap[layer]:
                    # if self.tilemap[layer][str_loc]['type'] not in self.non_collideables:
                    rects.append(pygame.Rect(tile_loc[0] * self.tile_size, tile_loc[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    # gets position in tiles
    def get_tile(self, pos, curr_layer=None):
        # tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        str_pos = str(pos[0]) + ';' + str(pos[1])
        if curr_layer:
            if str_pos in self.tilemap[curr_layer]:
                return True
        else:
            for layer in sorted([int(key) for key in self.tilemap.keys()]):
                layer = str(layer)
                if str_pos in self.tilemap[layer]:
                    return True
        
        
    
     
    def tile_collide(self, pos):
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
        for layer in sorted([int(key) for key in self.tilemap.keys()]):
            layer = str(layer)
            if tile_loc in self.tilemap[layer]:
                # if self.tilemap[layer][tile_loc]['type'] not in self.non_collideables: # for 
                return True
            
        
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
            if layer in sorted(self.tilemap):
                tile_loc = str(pos[0]) + ';' + str(pos[1])
                self.tilemap[layer][tile_loc] = tile
            else:
                self.tilemap[layer] = {} # if layer doesnt exist
    
    # gives grid positions (USES GRID POS)
    def remove_tile(self, tile, layer):
        pos = tile['pos']
        if layer in sorted(self.tilemap).copy():
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
                tile_r = pygame.Rect(*tile_data['pos'], self.tile_size, self.tile_size)
                if tile_r.collidepoint(curr_mpos):
                    self.offgrid_tiles[layer].remove(tile_data)
                
    # be careful of layer in self.tilemap because when converted from json the layer is in STRING          
    def render(self, surf, offset=(0, 0)):
        
        for layer in self.offgrid_tiles: # convert layer into int so it can be sorted then convert it back for proper layer opacity functionality
            tile_layer = self.offgrid_tiles[layer]
            for tile in tile_layer:
                surf.blit(self.game.assets.tiles[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for layer in sorted([int(key) for key in self.tilemap.keys()]): # 0
            layer = str(layer)
            tile_layer = self.tilemap[layer]
            # for loc in tile_layer:
            #     tile = tile_layer[loc]
            #     surf.blit(self.game.assets.tiles[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            for y in range(self.game.world.camera.pos[1] // self.tile_size, ((self.game.world.camera.pos[1] + surf.get_height()) // self.tile_size) + 1):
                for x in range(self.game.world.camera.pos[0] // self.tile_size, ((self.game.world.camera.pos[0] + surf.get_width()) // self.tile_size) + 1):
                    tile_loc = str(x) + ';' + str(y)
                    if tile_loc in tile_layer:
                        tile = tile_layer[tile_loc]
                        surf.blit(self.game.assets.tiles[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        
        
    
                
    def render_editor(self, curr_layer, layer_opacity, surf, offset=(0,0)):
        
        for layer in sorted([int(key) for key in self.offgrid_tiles.keys()]):
            layer = str(layer)
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
                                
        for layer in sorted([int(key) for key in self.tilemap.keys()]): 
            layer = str(layer)
            tile_layer = self.tilemap[layer]
            for loc in tile_layer:
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
                        
                        
        
                    
                    