import pygame
import random

from .tilemap import Tilemap
from .camera import Camera
from .entities import Entities
from .spark import SparkManager
from .projectile import ProjectileManager
from .particles import ParticleManager
from .inventory_menu import InventoryMenu
from .minimap import Minimap
from .config import config
from .item_notification import ItemNotification


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
        self.item_notifications = ItemNotification(game)
        
        self.inventory_menu = InventoryMenu(game, self.player.inventory)
        self.inventory_mode = False
        
        self.master_clock = 0
        self.transition = 0
        
        self.leaf_rects = []
        
    
    def environment_particles(self, surf):
        # leaf particles
        for tree in self.tilemap.extract_offgrid('trees'):
            # if the tree is visible on the players screen
            if (self.camera.pos[0] <=  tree['pos'][0] + self.game.assets.tiles['foliage'][0].get_width() <= (self.camera.pos[0] + surf.get_width())) or (self.camera.pos[0] <=  tree['pos'][0] <= (self.camera.pos[0] + surf.get_width())):
                r = pygame.Rect(tree['pos'][0] + 9, tree['pos'][1] + 8, 44, 17)
                if random.randint(0, 9999) < (r.width - r.height):
                    pos = [r.x + random.random() * r.width, r.y + random.random() * r.height]
                    color = (random.randint(100, 150), random.randint(80, 130), random.randint(10, 50))
                    self.particle_manager.add_particle(self.game, 'leaf', pos, [random.randint(-60, -35), random.randint(25, 35)], 0.8, random.randint(0, 2), color)
    
    def update(self):
        dt = self.game.window.dt
        self.master_clock += dt
        
        self.camera.update()
        self.entities.update(dt)
        self.minimap.update()
        self.particle_manager.update(dt)
        self.spark_manager.update(dt)
        self.projectile_manager.update(dt)
        self.item_notifications.update(dt)
            
    def render(self, surf):
        offset = self.camera.pos
        
        self.environment_particles(surf)
        
        self.tilemap.render(surf, offset=offset)
        self.entities.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.projectile_manager.render(surf, offset=offset)
        self.item_notifications.render(surf)
        
        
        
        
             
        