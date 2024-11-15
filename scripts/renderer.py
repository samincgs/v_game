import pygame

from scripts.background import Background


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        
    def render(self):
        surf = self.game.window.display

        health_bar_img = self.game.assets.misc['health_bar']

        # when not in the inventory
        if not self.game.world.inventory_mode:
        
            self.background.update()
            self.background.render(surf)
            
             # ammo ui
        self.game.assets.fonts['small_white'].render(str(self.game.world.player.weapon.ammo) + ' / ' + str(self.game.world.player.weapon.max_ammo), surf, (3, health_bar_img.get_height() + 5))
        
        # weapon display
        base_pos = 25
        offset = 0
        for ix, weapon in enumerate(self.game.world.player.inventory.get_active_weapons()):
            color = (255, 255, 255)
            curr_weapon = weapon.img.copy()
            weapon_mask = pygame.mask.from_surface(curr_weapon)
            weapon_rect = weapon_mask.get_bounding_rects()[0]
            if self.game.world.player.selected_weapon == ix:
                pygame.draw.line(surf, color, (2, base_pos + ix * offset), (2, base_pos + ix * offset + weapon_rect[3]), 2)
            else:
                color = (139, 171, 191)
            weapon_mask = weapon_mask.to_surface(setcolor=color, unsetcolor=(0,0,0,0))
            surf.blit(weapon_mask, (2, base_pos + ix * offset))
            offset += 10

        
        #health bar
        pygame.draw.rect(surf, 'red', pygame.Rect(1, 2, int((self.game.world.player.health / self.game.world.player.max_health * 55)), 9)) # TODO: change to darker red
        surf.blit(health_bar_img,(1, 2))   
        
        self.game.world.render(surf)
        
        if self.game.world.inventory_mode:
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
        
        