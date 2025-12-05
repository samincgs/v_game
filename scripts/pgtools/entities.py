import pygame

from .utils import outline, collision_check

class Entity:
    def __init__(self, game, pos, size, e_type):
        self.game = game
        self.pos = list(pos)
        self.size = list(size)
        self.type = e_type
        
        self.active_animation = None
        self.action = None
        
        self.rotation = 0
        self.flip = [False, False]
        self.outline = False
        self.alpha = False
        
        if not self.active_animation:
            self.set_action('idle')
           
    @property
    def img(self):
        if self.active_animation:
            img = self.active_animation.img
            if self.active_animation.outline:
                self.outline = self.active_animation.outline
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.alpha:
            img.set_alpha(self.alpha)
        return img

          
    @property 
    def center(self):
        return self.rect.center
    
    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    @property
    def animations(self):
        animations = None
        try:
            animations = self.game.animations
        except AttributeError:
            animations = self.game.assets.animations
        return animations
    
    @property 
    def anim_offset(self):
        offset = (0, 0)
        if self.active_animation:
            offset = self.active_animation.animation['offset']
        return offset

    @property
    def rotation_offset(self):
        offset = (0, 0)
        base_img = self.active_animation.img
        if self.rotation:
            base_img_size = base_img.get_size()
            rotated_size = self.img.get_size()
            size_diff = (rotated_size[0] - base_img_size[0], rotated_size[1] - base_img_size[1])
            offset = (size_diff[0] // 2, size_diff[1] // 2)            
        return offset
        
    def set_action(self, action, force=False):
        if force or action != self.action:
            self.action = action
            self.active_animation = self.animations.new(self.type + '/' + self.action)
    
    def update(self, dt):
        if self.active_animation:
            self.active_animation.update(dt)
    
    def render(self, surf, offset=(0, 0)):
        render_pos = (int(self.pos[0] - offset[0] + self.anim_offset[0] - self.rotation_offset[0]), int(self.pos[1] - offset[1] + self.anim_offset[1] - self.rotation_offset[1]))
        if self.outline:
            outline(surf, self.img, render_pos, self.outline)
        surf.blit(self.img, render_pos)
        
class PhysicsEntity(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.speed = 0
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.frame_movement = [0, 0]
        self.last_movement = [0, 0]
        
        self.collision_directions = {'up': False, 'down': False, 'right': False, 'left': False}

    @property
    def physics_rect(self):
        return pygame.FRect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def move(self, movement, dt):
        self.frame_movement[0] += movement[0] * dt
        self.frame_movement[1] += movement[1] * dt
        self.last_movement = self.frame_movement.copy()
    
    def physics_movement(self, tilemap, movement=(0, 0)):
        self.collision_directions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # horizontal
        self.pos[0] += movement[0]
        entity_rect = self.physics_rect
        collision_rects = []
        if tilemap:
            tile_rects = tilemap.get_nearby_rects(self.center)
            collision_rects = collision_check(self.physics_rect, tile_rects)
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
            collision_rects = collision_check(self.physics_rect, tile_rects)
        for tile_rect in collision_rects:
            if movement[1] > 0:
                entity_rect.bottom = tile_rect.top
                self.pos[1] = entity_rect.y
                self.collision_directions['down'] = True
            if movement[1] < 0:
                entity_rect.top = tile_rect.bottom
                self.pos[1] = entity_rect.y
                self.collision_directions['up'] = True  

        self.frame_movement = [0, 0]
            
        
                    
            
        
            
 
                    
        
        
        
        

            
        
                
        

                
        

        

            
