import pygame

import scripts.pgtools as pt


DROPTHROUGH_SIZE = (16, 9)

class Tilemap(pt.Tilemap):
    def __init__(self, game, tile_size=16):
        super().__init__(game, tile_size)
        self.dropthroughs = []
    
    def load_map(self, path):
        map_data = pt.utils.load_json(path)
        
        self.tilemap = map_data['tilemap'] 
        self.offgrid_tiles = map_data['offgrid_tiles']
        self.dropthroughs = self.extract(('structures', (0, 1)), keep=True, offgrid=False)

    def get_dropthrough_rects(self):
        rects = []
        for dropthrough in self.dropthroughs:
            r = pygame.Rect(dropthrough['tile_pos'][0] * self.tile_size, dropthrough['tile_pos'][1] * self.tile_size, DROPTHROUGH_SIZE[0], DROPTHROUGH_SIZE[1])
            rects.append(r)
        return rects
        
    