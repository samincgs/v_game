import scripts.pgtools as pt

from .entities import Entities
from .spark import SparkManager
from .projectile import ProjectileManager
from .particles import ParticleManager
from .inventory_menu import InventoryMenu


class World:
    def __init__(self, game):
        self.game = game
        self.map_area = 'map_3'
        self.tilemap = pt.Tilemap(game, tile_size=16) # tile_size is 16
        self.tilemap.load_map('data/maps/' + self.map_area + '.json')
        self.entities = Entities(game)
        self.entities.load_entities(self.tilemap)
        self.player = self.entities.player 
        self.camera = pt.Camera(self.game.window.display.get_size(), tile_size=16, lag=30)
        self.camera.set_target(self.player)
        self.particle_manager = ParticleManager(game)
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
        
        self.inventory_menu = InventoryMenu(game, self.player.inventory)
        self.inventory_mode = False
        
        self.master_clock = 0
        self.transition = 0
        self.initial_spawn = True
        self.show_fps = False
    
    def start_transition(self, map_id):
        self.transition = 1
        self.map_area = map_id
         
    def load_level(self, new=False):
        self.tilemap.load_map('data/maps/' + self.map_area + '.json')
        self.entities = Entities(self.game)
        self.entities.load_entities(self.tilemap)
        self.player = self.entities.player
        self.camera.set_target(self.player)
        self.particle_manager = ParticleManager(self.game)
        self.spark_manager = SparkManager()
        self.projectile_manager = ProjectileManager()
        self.camera.snap_to_target()
    
    def update(self):        
        if self.game.input.pressing('fps'):
            self.show_fps = not self.show_fps
        if self.game.input.pressing('screen_toggle'):
            self.game.window.toggle_window()
                    
        dt = self.game.window.dt
        self.master_clock += dt
                
        if self.transition:
            if self.transition > 0:
                self.transition = min(self.transition + 60 * dt, 30)
            if self.transition < 0:
                self.transition = min(self.transition + 60 * dt, 0)
            if self.transition == 30:
                self.transition = -30
                self.load_level()

        self.camera.update()
        self.entities.update(dt)
        self.particle_manager.update(dt)
        self.spark_manager.update(dt)
        self.projectile_manager.update(dt)
            
    def render(self, surf, offset=(0, 0)):
        self.entities.tile_render(surf, offset=offset)
        self.tilemap.render_visible(surf, visible_range=self.camera.get_visible_screen, offset=offset)
        self.entities.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.projectile_manager.render(surf, offset=offset)
        
        
        
        
        
        
        
        
             
        