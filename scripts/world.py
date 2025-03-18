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
        self.map_area = 'test'
        
        self.camera = Camera(game)
        self.tilemap = Tilemap(game, tile_size=config['window']['tile_size']) # tile_size is 16
        self.tilemap.load_map('data/maps/' + self.map_area + '.json')
        self.entities = Entities(game)
        self.tilemap.load_destructables(self.entities)
        self.player = self.entities.player
        self.camera.set_tracked_entity(self.player)
        self.minimap = Minimap(game, tile_size=config['window']['tile_size'])
        self.particle_manager = ParticleManager(game)
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
        self.item_notifications = ItemNotification(game)
        
        self.inventory_menu = InventoryMenu(game, self.player.inventory)
        self.inventory_mode = False
        
        self.master_clock = 0
        self.transition = 0
        
        
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
                
        self.tilemap.render_visible(surf, offset=offset)
        self.entities.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.projectile_manager.render(surf, offset=offset)
        self.item_notifications.render(surf)
        
        
        
        
             
        