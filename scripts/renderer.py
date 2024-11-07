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
        
        # world_surf = pygame.Surface(surf.get_size())
        # world_surf.set_colorkey((0, 0, 0))
        
        #health bar
        health_bar_img = self.game.assets.misc['health_bar']
        pygame.draw.rect(surf, 'red', pygame.Rect(1, 2, int((self.game.world.player.health / self.game.world.player.max_health * 55)), 9)) # TODO: change to darker red
        surf.blit(health_bar_img,(1, 2))
        
        # ammo ui
        self.game.assets.fonts['small_white'].render(str(self.game.world.player.weapon.ammo) + ' / ' + str(self.game.world.player.weapon.max_ammo), surf, (3, health_bar_img.get_height() + 5))
        
        
        # world_mask = pygame.mask.from_surface(world_surf)
        # world_bg = world_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(0, 0, 0, 255))
        # surf.blit(world_bg, (2, 3))
        # surf.blit(world_surf, (0, 0))