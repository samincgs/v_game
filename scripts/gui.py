import random
import time
import pygame

class GUI:
    def __init__(self, game):
        self.game = game
        
    
    def render_stats(self, surf, assets, player):
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
                
            weapon_surface = weapon_mask.to_surface(setcolor=color, unsetcolor=(0,0,0,0))
            
            
            surf.blit(weapon_surface, (2, base_pos + offset))
            offset += weapon_surface.get_height() + 3
     
          
        # skills
        skill_offset = 20
        
        for skill in self.game.world.player.skills:
            
            # skill placement holders
            surf.blit(assets.misc['skill_holder'], (skill_offset, surf.get_height() - assets.misc['skill_holder'].get_height()))
            skill_offset += assets.misc['skill_holder'].get_width() - 7
            
            skill_img = skill.img.copy()
            if skill.amount >= 1:
                assets.fonts['small_white'].render(surf, str(skill.amount), (30, surf.get_height() - assets.misc['skill_holder'].get_height() - 6))
            else:
                dash_cooldown = skill.charge / skill.charge_rate
                dash_cooldown_surf = pygame.Surface((skill_img.get_width(), skill_img.get_height() * (1 - dash_cooldown)))
                dash_cooldown_surf.fill((120, 120, 120))
                            
                skill_img.blit(dash_cooldown_surf, (0, skill_img.get_height() - dash_cooldown_surf.get_height()), special_flags=pygame.BLEND_RGB_MULT)
                
            surf.blit(skill_img, (24, surf.get_height() - assets.misc['skill_holder'].get_height() + 5))
    
    
    # def render_input(self, surf, assets):
    #     left_input = assets.misc['left_mouse_input']
    #     surf.blit(left_input, (38, self.game.window.display.get_height() - left_input.get_height()))
    
    def render_minimap(self, surf, assets):
         
        dark_surf = pygame.Surface(self.game.world.minimap.map_surf.get_size())
        dark_surf.fill((30, 30, 40)) 
        
        # minimap
        surf.blit(dark_surf, (323, 2), special_flags=pygame.BLEND_RGBA_MULT) # fix the blending and make it transparent
        surf.blit(self.game.world.minimap.map_surf, (323, 2))
        surf.blit(assets.misc['minimap'], (317, 0))
    
    def render(self, surf):
        
        assets = self.game.assets
        player = self.game.world.player

        self.render_stats(surf, assets, player)
        # self.render_input(surf, assets)
        self.render_minimap(surf, assets)
             
        # show fps
        if self.game.input.show_fps:
            assets.fonts['small_white'].render(surf, 'FPS: ' + str(int(self.game.window.fps)), (surf.get_width() - 35, 2))
            print(str(int(self.game.window.fps)))
        