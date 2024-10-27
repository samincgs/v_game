import pygame

from .tilemap import Tilemap

class World:
    def __init__(self, game):
        self.game = game
        
        self.tilemap = Tilemap(game, 16, self.game.window.display.get_size())
        self.tilemap.load_map('data/maps/main.json')
        
        
    def update(self):
        pass
    
    def render(self, surf):
        self.tilemap.render(surf)