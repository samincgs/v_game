import pygame
from scripts.background import Background
from scripts.gui import GUI
from scripts.minimap import Minimap
from scripts.tooltips import Tooltips
from scripts.settings_menu import SettingsMenu


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        self.minimap = Minimap(game, tile_size=16)
        self.settings_menu = SettingsMenu(game)
        self.gui = GUI(game)
        self.tooltips = Tooltips(game)
        

    def render(self):
        surf = self.game.window.display
        offset = self.game.world.camera.pos
            
        if not self.game.window.pause_state:
            self.background.update()
            self.minimap.update()
            self.tooltips.update(self.game.window.dt)
            
        self.background.render(surf)
        self.game.world.render(surf, offset)
        self.gui.render(surf)
        self.tooltips.render(surf, offset)
        
        dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
        dark_overlay.fill((31, 33, 54, 170))  #TODO: try diff colors
        
                    
        if self.game.window.show_settings:
            dark_overlay.fill((16, 21, 37, 220)) 
            surf.blit(dark_overlay, (0, 0))
            self.settings_menu.update_render(surf=surf)
        
        # inventory
        if self.game.window.inventory_mode:
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
        

        
        
            
        
        