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
                  
        self.background.update()
        self.background.render(surf)
    
        self.game.world.render(surf)
        self.gui.render(surf)
        
        # inventory
        if self.game.world.inventory_mode:
            dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
            dark_overlay.fill((31, 33, 54, 170)) # try different colours
            surf.blit(dark_overlay, (0, 0))
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
        

        
        
            
        
        