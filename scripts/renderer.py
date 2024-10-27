import pygame

from scripts.background import Background


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        
    def render(self):
        surf = self.game.window.display
        
        self.background.update()
        self.background.render(surf)
        self.game.world.render(surf)
        
        world_surf = pygame.Surface(surf.get_size())
        world_surf.set_colorkey((0, 0, 0))
        
        # world_mask = pygame.mask.from_surface(world_surf)
        # world_bg = world_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(0, 0, 0, 255))
        # surf.blit(world_bg, (2, 3))
        # surf.blit(world_surf, (0, 0))