import pygame

from scripts.background import Background


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)

    def gui(self, surf):
        # ammo ui
        self.game.assets.fonts['small_white'].render(str(self.game.world.player.weapon.ammo) + ' / ' + str(self.game.world.player.weapon.max_ammo), surf, (3, 14))
    
        #health bar
        health_bar_img = self.game.assets.misc['health_bar']
        pygame.draw.rect(surf, (215, 0, 40), pygame.Rect(1, 2, int((self.game.world.player.health / self.game.world.player.max_health * 55)), 9)) 
        surf.blit(health_bar_img,(1, 2))
        
         # weapon display
        base_pos = 25
        offset = 0
        for ix, weapon in enumerate(self.game.world.player.inventory.get_active_weapons()):
            color = (255, 255, 255)
            curr_weapon = weapon.img.copy()
            weapon_mask = pygame.mask.from_surface(curr_weapon)
            weapon_rect = weapon_mask.get_bounding_rects()[0]
            if self.game.world.player.selected_weapon == ix:
                pass
                pygame.draw.line(surf, color, (2, base_pos + offset), (2, base_pos + offset + weapon_rect[3]), 2)
            else:
                color = (139, 171, 191)
            weapon_mask = weapon_mask.to_surface(setcolor=color, unsetcolor=(0,0,0,0))
            surf.blit(weapon_mask, (2, base_pos + offset))
            offset += 15
            
    
    def render(self):
        surf = self.game.window.display
                  
        # self.background.update()
        # self.background.render(surf)
                    
        
        self.gui(surf)
        self.game.world.render(surf)
        
        if self.game.world.inventory_mode:
            dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
            dark_overlay.fill((31, 33, 54, 110)) # try different colours
            surf.blit(dark_overlay, (0, 0))
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
        
          
        if self.game.input.show_fps:
            self.game.assets.fonts['small_white'].render('FPS: ' + str(int(self.game.window.fps)), surf, (surf.get_width() - 35, 2))
            
        
        