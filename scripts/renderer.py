import math
import pygame
import random
from scripts.background import Background
from scripts.gui import GUI
from scripts.minimap import Minimap
from scripts.tooltips import Tooltips


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        self.minimap = Minimap(game, tile_size=16)
        self.gui = GUI(game)
        self.tooltips = Tooltips(game)
        

    def render(self):
        surf = self.game.window.display
        offset = self.game.world.camera.pos
                  
        self.background.update()
        self.background.render(surf)
    
        self.game.world.render(surf, offset)
                
        self.minimap.update()

        self.gui.render(surf)
        
        self.tooltips.update(self.game.window.dt)
        self.tooltips.render(surf, offset)
            
        # inventory
        if self.game.world.inventory_mode:
            dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
            dark_overlay.fill((31, 33, 54, 170)) # try different colours
            surf.blit(dark_overlay, (0, 0))
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
            
            
        # transition
        transition = self.game.world.transition
        if transition:
            transition_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            if transition > 0:
                alpha = int((transition / 30) * 255)
            else:
                alpha = int((abs(transition) / 30) * 255)
            
            transition_surf.fill((0, 0, 0, alpha))
            surf.blit(transition_surf, (0, 0))
        

        
        
            
        
        