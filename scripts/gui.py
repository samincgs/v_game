import pygame

class GUI:
    def __init__(self, game):
        self.game = game

    
    def render(self, surf):
        
        assets = self.game.assets
        player = self.game.world.player
        
        # ammo ui
        if player.weapon:
            assets.fonts['small_white'].render(surf, str(player.weapon.ammo) + ' / ' + str(player.weapon.max_ammo), (3, 14))
    
        #health bar
        health_bar_img = assets.misc['health_bar']
        pygame.draw.rect(surf, (215, 0, 40), pygame.Rect(1, 2, int((player.health / player.max_health * 55)), 9)) 
        surf.blit(health_bar_img,(1, 2))
        
         # weapon display
        base_pos = 25
        offset = 0
        for ix, weapon in enumerate(player.inventory.get_active_weapons()):
            color = (255, 255, 255)
            curr_weapon = weapon.img.copy()
            weapon_mask = pygame.mask.from_surface(curr_weapon)
            weapon_rect = weapon_mask.get_bounding_rects()[0]
            if player.selected_weapon == ix:
                pygame.draw.line(surf, color, (2, base_pos + offset), (2, base_pos + offset + weapon_rect[3]), 2)
            else:
                color = (139, 171, 191)
            weapon_mask = weapon_mask.to_surface(setcolor=color, unsetcolor=(0,0,0,0))
            surf.blit(weapon_mask, (weapon_rect.left, base_pos + offset))
            offset += weapon_mask.get_height() + 3
     
          
        # skills
        skill_offset = 20
        for i in range(1):
            surf.blit(assets.misc['skill_holder'], (skill_offset, surf.get_height() - assets.misc['skill_holder'].get_height()))
            skill_offset += assets.misc['skill_holder'].get_width()
        
        
        dash_img = assets.misc['dash'].copy()
        
        if player.dashes >= 1:
            assets.fonts['small_white'].render(surf, str(player.dashes), (30, surf.get_height() - assets.misc['skill_holder'].get_height() - 6))
        else:
            dash_cooldown = player.dash_charge / player.dash_charge_rate
            dash_cooldown_surf = pygame.Surface((dash_img.get_width(), dash_img.get_height() * (1 - dash_cooldown)))
            dash_cooldown_surf.fill((120, 120, 120))
            dash_img.blit(dash_cooldown_surf, (0, dash_img.get_height() - dash_cooldown_surf.get_height()), special_flags=pygame.BLEND_RGB_MULT)
            
        surf.blit(dash_img, (24, surf.get_height() - assets.misc['skill_holder'].get_height() + 5))
        
        # minimap
        surf.blit(self.game.world.minimap.map_surf, (323, 2))
        surf.blit(assets.misc['minimap'], (317, 0))
        
        # inventory
        if self.game.world.inventory_mode:
            dark_overlay = pygame.Surface(surf.get_size(), flags=pygame.SRCALPHA)
            dark_overlay.fill((31, 33, 54, 110)) # try different colours
            surf.blit(dark_overlay, (0, 0))
            self.game.world.inventory_menu.update()
            self.game.world.inventory_menu.render(surf)
        
        # show fps
        if self.game.input.show_fps:
            assets.fonts['small_white'].render(surf, 'FPS: ' + str(int(self.game.window.fps)), (surf.get_width() - 35, 2))
            print(str(int(self.game.window.fps)))
        