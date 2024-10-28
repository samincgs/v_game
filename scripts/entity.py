import pygame

from .config import config

class Entity:
    def __init__(self, game, pos, size, e_type):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = list(size)
        self.max_health = config['entities'][e_type]['base_health']
        self.health = self.max_health
        self.flip = [False, False]
        self.hurt = 0
        self.centered = False