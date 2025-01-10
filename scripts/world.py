import pygame

from .tilemap import Tilemap
from .camera import Camera
from .entities import Entities
from .spark import SparkManager
from .projectile import ProjectileManager
from .particles import ParticleManager
from .inventory_menu import InventoryMenu
from .minimap import Minimap
from .config import config


class World:
    def __init__(self, game):
        self.game = game
        self.map_area = 'intro'
        
        self.camera = Camera(game)
        self.tilemap = Tilemap(game, tile_size=config['window']['tile_size']) # tile_size is 16
        self.tilemap.load_map('data/maps/' + self.map_area + '.json')
        self.entities = Entities(game)
        self.player = self.entities.player
        self.camera.set_tracked_entity(self.player)
        self.minimap = Minimap(game, tile_size=config['window']['tile_size'])
        self.particle_manager = ParticleManager()
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
        
        self.inventory_menu = InventoryMenu(game, self.player.inventory)
        self.inventory_mode = False
        
        self.master_clock = 0
        self.transition = 0
        
        self.portal_rect = pygame.Rect(*self.tilemap.extract_offgrid('portal'), 9, 16)
        
        self.portal_collided = False
    
    def reset_level(self):
        self.entities = Entities(self.game)
        self.player = self.entities.player
        self.camera.set_tracked_entity(self.player)
        self.master_clock = 0
        self.tilemap = Tilemap(self.game, tile_size=config['window']['tile_size'])
        self.tilemap.load_map('data/maps/' + self.map_area + '.json')
        self.particle_manager = ParticleManager()
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
        self.inventory_menu = InventoryMenu(self.game, self.player.inventory)
        self.minimap = Minimap(self.game, tile_size=config['window']['tile_size'])
        self.camera.focus()
        
        
    def update(self):
        dt = self.game.window.dt
        self.master_clock += dt
        
        if self.transition:
            self.transition = max(self.transition - dt * 45, -20)
            if self.transition < -5:
                self.reset_level()
            if self.transition == -20:
                self.transition = 0
            
        
        self.camera.update()
        self.entities.update(dt)
        self.minimap.update()
        self.particle_manager.update(dt)
        self.spark_manager.update(dt)
        self.projectile_manager.update(dt)
        
        
        if self.player.rect.colliderect(self.portal_rect) and not self.portal_collided:
            self.portal_collided = True
            self.transition = 20
            self.map_area = 'intro_2'
            
                
    def render(self, surf):
        offset = self.camera.pos
        self.tilemap.render(surf, offset=offset)
        self.entities.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.projectile_manager.render(surf, offset=offset)
    
        
        
            
        