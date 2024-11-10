from .tilemap import Tilemap
from .camera import Camera
from .player import Player
from .spark import SparkManager
from .particle import ParticleManager
from .vfx import VFX

class World:
    def __init__(self, game):
        self.game = game
        self.camera = Camera(game)
        self.tilemap = Tilemap(game, 16, self.game.window.display.get_size())
        self.tilemap.load_map('data/maps/intro.json')
        self.player = Player(game, (200, 200), (8, 17), 'player')
        self.camera.set_tracked_entity(self.player)
        self.particle_manager = ParticleManager()
        self.spark_manager = SparkManager()
        self.vfx = VFX()
        
        self.projectiles = []
        
    def update(self):
        dt = self.game.window.dt
        self.camera.update()
        self.player.update(dt)
        self.particle_manager.update(dt)
        self.spark_manager.update(dt)
        self.vfx.update(dt)
        
        for proj in self.projectiles.copy():
            kill = proj.update(dt)
            proj.render(self.game.window.display, self.game.world.camera.pos)
            if kill:
                self.projectiles.remove(proj)
    
        
    
    def render(self, surf):
        offset = self.camera.pos
        self.tilemap.render(surf, offset=offset)
        self.player.render(surf, offset=offset)
        self.particle_manager.render(surf, offset=offset)
        self.spark_manager.render(surf, offset=offset)
        self.vfx.render(surf, offset=offset)
        # pygame.draw.rect(surf, 'red', pygame.Rect(self.player.center[0] - offset[0], self.player.center[1] - offset[1], 1, 1)) # debug
        