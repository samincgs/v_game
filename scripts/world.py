from .tilemap import Tilemap
from .camera import Camera
from .entities import Entities
from .spark import SparkManager
from .projectile import ProjectileManager
from .particle import ParticleManager
from .inventory_menu import InventoryMenu
from .itemdrop import Itemdrop

class World:
    def __init__(self, game):
        self.game = game
        self.camera = Camera(game)
        self.tilemap = Tilemap(game, tile_size=16)
        self.tilemap.load_map('data/maps/intro.json')
        self.entities = Entities(game)
        self.player = self.entities.player
        self.camera.set_tracked_entity(self.player)
        self.particle_manager = ParticleManager()
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
 
        self.inventory_menu = InventoryMenu(game, self.player.inventory)
        self.inventory_mode = False
        
        self.item_drops = []
  
    def update(self):
        dt = self.game.window.dt
        self.camera.update()
        self.entities.update(dt)
        self.particle_manager.update(dt)
        self.spark_manager.update(dt)
        self.projectile_manager.update(dt)
        
        for item in self.item_drops:
            item.update(dt)
        
    
    def drop_item(self, item, pos, velocity):
        self.item_drops.append(Itemdrop(self.game, pos, (1, 1), 'item', item, velocity))
                    
    def render(self, surf):
        offset = self.camera.pos
        self.tilemap.render(surf, offset=offset)
        self.entities.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.projectile_manager.render(surf, offset=offset)
        # pygame.draw.rect(surf, 'red', pygame.Rect(self.player.center[0] - offset[0], self.player.center[1] - offset[1], 1, 1)) # debug
        
        for item in self.item_drops:
            item.render(surf, offset=offset)
        
        # inventory_surf = surf.copy()
        
            
        # surf.blit(surf, (0, 0))
        