import pygame

from .tilemap import Tilemap
from .camera import Camera
from .player import Player

class World:
    def __init__(self, game):
        self.game = game
        self.camera = Camera(game)
        self.tilemap = Tilemap(game, 16, self.game.window.display.get_size())
        self.tilemap.load_map('data/maps/main.json')
        self.player = Player(game, (200, 200), (8, 17), 'player')
        self.camera.set_tracked_entity(self.player)
        
    def update(self):
        self.camera.update()
        self.player.update(self.game.window.dt)
    
    def render(self, surf):
        self.tilemap.render(surf, offset=self.camera.pos)
        self.player.render(surf, offset=self.camera.pos)