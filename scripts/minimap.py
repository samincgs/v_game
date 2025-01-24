import pygame

class Minimap:
    def __init__(self, game, tile_size):
      self.game = game
      self.tile_size = tile_size
      
      self.minimap_data = {}
      self.chunk_size = 4
      self.chunk_pixels = self.chunk_size * self.tile_size
      
      self.size = (58, 47)
      self.map_surf = pygame.Surface(self.size)
      
    def generate_map_chunk(self, chunk_pos):
        chunk_surf = pygame.Surface((self.chunk_size, self.chunk_size))
        base_pos = (chunk_pos[0] * self.chunk_size, chunk_pos[1] * self.chunk_size) # tile pos
        for y in range(self.chunk_size):
            for x in range(self.chunk_size):
                tile_pos = (base_pos[0] + x, base_pos[1] + y) # tile pos
                if self.game.world.tilemap.get_tile(tile_pos):
                    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
                    for d in directions:
                        if not self.game.world.tilemap.get_tile((base_pos[0] + x + d[0], base_pos[1] + y + d[1])):
                            chunk_surf.set_at((x, y), (80, 90, 100))
        self.minimap_data[chunk_pos] = chunk_surf
    
    def update(self):
        self.map_surf = pygame.Surface(self.size)
                
        camera_pos = self.game.world.camera.pos
        display_w, display_h = self.game.window.display.get_width(), self.game.window.display.get_height()
        
        chunk_pos = (int(camera_pos[0] // self.chunk_pixels), int(camera_pos[1] // self.chunk_pixels))
        
        # if chunk pos is not in minimap data, we generate them
        for y in range(display_h // self.chunk_pixels + 1):
            for x in range(display_w // self.chunk_pixels + 1):
                target_pos = (chunk_pos[0] + x, chunk_pos[1] + y)
                if target_pos not in self.minimap_data:
                    self.generate_map_chunk(target_pos)
        
        offset = [(self.size[0] * self.tile_size - display_w) / 2, (self.size[1] * self.tile_size - display_h) / 2]
        render_pos = (int((camera_pos[0] - offset[0]) // self.chunk_pixels), int((camera_pos[1] - offset[1]) // self.chunk_pixels))
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                target_pos = (render_pos[0] + x, render_pos[1] + y)
                if target_pos in self.minimap_data:
                    self.map_surf.blit(self.minimap_data[target_pos], (render_pos[0] * self.chunk_size - (camera_pos[0] - offset[0]) // self.tile_size + x * self.chunk_size, render_pos[1] * self.chunk_size - (camera_pos[1] - offset[1]) // self.tile_size + y * self.chunk_size))
        
        self.map_surf.set_colorkey((0, 0, 0))
        
        # add indicators
        for entity in self.game.world.entities.entities:
            p = [int(entity.center[0] // self.tile_size - (camera_pos[0] - offset[0]) // self.tile_size), int(entity.center[1] // self.tile_size - (camera_pos[1] - offset[1]) // self.tile_size)]
            if entity == self.game.world.entities.player:
                c = (255, 255, 255)
            elif entity.type == 'item':
                c = (156, 216, 252)
            elif entity.type == 'crate':
                c = (64, 209, 25)
            else:
                c = (255, 0, 0)
            self.map_surf.set_at(p, c)
        
        
        