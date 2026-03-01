from scripts.entity import Entity
import scripts.pgtools as pt


class PhysicsEntity(Entity, pt.PhysicsEntity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        
        self.gravity = 600
        self.terminal_velocity = 400
        self.horizontal_normalization = 250
        self.dropthrough = False

    
    def physics_movement(self, tilemap, movement=(0, 0)):
        self.collision_directions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # horizontal
        self.pos[0] += movement[0]
        entity_rect = self.physics_rect
        collision_rects = []
        if tilemap:
            tile_rects = tilemap.get_nearby_rects(self.center)
            collision_rects = pt.utils.collision_check(self.physics_rect, tile_rects)
        for tile_rect in collision_rects:
            if movement[0] > 0:
                entity_rect.right = tile_rect.left
                self.pos[0] = entity_rect.x
                self.collision_directions['right'] = True
            if movement[0] < 0:
                entity_rect.left = tile_rect.right
                self.pos[0] = entity_rect.x
                self.collision_directions['left'] = True
                  
        # vertical   
        self.pos[1] += movement[1]
        entity_rect = self.physics_rect
        collision_rects = []
        if tilemap:
            tile_rects = tilemap.get_nearby_rects(self.center)
            if self.dropthrough:
                dropthrough_rects = tilemap.get_dropthrough_rects()
                tile_rects += dropthrough_rects
            collision_rects = pt.utils.collision_check(self.physics_rect, tile_rects)
        for tile_rect in collision_rects:
            if self.dropthrough:
                if tile_rect in dropthrough_rects:
                    if self.dropthrough_timer:
                        continue 
                if movement[1] < 0:
                    if self.rect.bottom >= tile_rect.top:
                        continue            
            if movement[1] > 0:
                entity_rect.bottom = tile_rect.top
                self.pos[1] = entity_rect.y
                self.collision_directions['down'] = True
            if movement[1] < 0:
                entity_rect.top = tile_rect.bottom
                self.pos[1] = entity_rect.y
                self.collision_directions['up'] = True  
        
                    

        self.frame_movement = [0, 0]
    
    def update(self, dt):
        r = super().update(dt)
        
        self.velocity[0] = pt.utils.normalize(self.velocity[0], self.horizontal_normalization * dt)
        self.velocity[1] = min(self.terminal_velocity, self.velocity[1] + dt * self.gravity)
        
        self.frame_movement[0] = self.velocity[0] * dt
        self.frame_movement[1] = self.velocity[1] * dt
        
        self.physics_movement(self.game.world.tilemap, self.frame_movement)
        
        return r
        