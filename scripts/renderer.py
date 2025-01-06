import pygame
from scripts.background import Background
from scripts.gui import GUI


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        self.gui = GUI(game)

    def render(self):
        surf = self.game.window.display
                  
        # self.background.update()
        # self.background.render(surf)
    
        self.game.world.render(surf)
        self.gui.render(surf)
        
        # inventory
        if self.game.world.inventory_mode:
            dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
            dark_overlay.fill((31, 33, 54, 110)) # try different colours
            surf.blit(dark_overlay, (0, 0))
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
        
        
        if self.game.world.transition:
            transition_surf = pygame.Surface(self.game.window.display.get_size())
            transition_surf.set_colorkey((255, 255, 255))
            pygame.draw.circle(transition_surf, (255, 255, 255), (self.game.window.display.get_width() // 2, self.game.window.display.get_height() // 2), (abs(self.game.world.transition) * 12))
            surf.blit(transition_surf, (0, 0))
        
        
            
        
        