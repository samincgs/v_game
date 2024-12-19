import pygame

from scripts.weapon import Weapon

from .config import config


class InventoryMenu:
    def __init__(self, game, inventory):
        self.game = game
        self.inventory = inventory
        self.rows, self.cols = 4, 4
        self.size = 25 # size of each box
        self.config = config['items']
        
        self.base_pos = [80, 40]
        self.border_radius = 3
        self.item_boxes = [] # [[rect of box, weapon/item name]]
        self.weapon_boxes = [] # 
        self.info = [] # [[item name (from config), item description, weapon/item name (weapon type), item_type]]
        
        
        
    def draw_weapon_boxes(self, surf):
        surf.blit(self.game.assets.misc['weapons_logo'], (self.base_pos[0] - self.game.assets.misc['weapons_logo'].get_width() + 3, self.base_pos[1]))

        self.weapon_boxes = []
        # weapon boxes
        for i in range(self.cols):
            rect = pygame.Rect(self.base_pos[0] + i * self.size, self.base_pos[1], self.size, self.size)
            color = (154, 170, 186)
            for ix, weapon in enumerate(self.inventory.get_active_weapons()):
                if ix == i:
                    weapon_img = self.game.assets.weapons[weapon.name]
                    color = (255, 255, 255)
                    surf.blit(weapon_img, (rect.centerx - weapon_img.get_width() // 2 - 2, rect.centery - weapon_img.get_height() // 2 ))
                    self.weapon_boxes.append([rect, weapon])
            
            pygame.draw.rect(surf, color, rect, 1, self.border_radius)
        
    
    
    def draw_item_boxes(self, surf):
        # item logo
        surf.blit(self.game.assets.misc['items_logo'], (self.base_pos[0] - self.game.assets.misc['weapons_logo'].get_width() + 3, self.base_pos[1] + 40))
        
        self.item_boxes = []
         # item boxes
        for i in range(self.rows):
            item_pos = [self.base_pos[0], self.base_pos[1] + 40]
            for j in range(self.cols):
                color = (154, 170, 186)
                rect = pygame.Rect(item_pos[0] + j * self.size, item_pos[1] + i * self.size, self.size, self.size)
                for ix, item in enumerate(self.inventory.get_items()):
                    if ix == j + i * self.cols:
                        color = (255, 255, 255)
                        item_img = self.game.assets.weapons[item.name] if item.type == 'weapon' else self.game.assets.items[item.name]
                        surf.blit(item_img, (rect.centerx - item_img.get_width() // 2, rect.centery - item_img.get_height() // 2))
                        if item.amount > 1:
                            self.game.assets.fonts['small_white'].render(str(item.amount), surf, (rect.centerx + 3.5, rect.centery + 5)) # name
                            
                        self.item_boxes.append([rect, item])
                    
                pygame.draw.rect(surf, color, rect, 1, self.border_radius)
                
            item_pos[1] += self.size
    
    def draw_ui(self, surf):  
        self.draw_weapon_boxes(surf)
        self.draw_item_boxes(surf)
                    
    def draw_info(self, info, surf, loc):
        img = self.game.assets.weapons[info.name] if isinstance(info, Weapon) else self.game.assets.items[info.name]
        name = self.config[info.name]['name']
        desc = self.config[info.name]['description']
        
        surf.blit(img, loc)
        self.game.assets.fonts['small_white'].render(name, surf, (loc[0] + img.get_width() + 5, loc[1])) # name
        self.game.assets.fonts['small_white'].render(desc, surf, (loc[0], loc[1] + 20), line_width=3) # description
    
    
    def update(self):
        self.info = []
        clicked = False
          
        for box in self.weapon_boxes:
            if box[0].collidepoint(self.game.input.mpos):
                self.info = box[1] 
                if not clicked and self.game.input.mouse_states['shoot']:
                    clicked = True
                    if len(self.inventory.get_active_weapons()) > 1:
                        for weapon in self.inventory.get_active_weapons():
                            if weapon.name == self.info.name:
                                weapon.remove_active()
                                self.game.world.player.slot_weapon(-1)
                                return
                            
        for box in self.item_boxes:
            if box[0].collidepoint(self.game.input.mpos):
                self.info = box[1] 
                if not clicked and self.game.input.mouse_states['shoot']:
                    clicked = True
                    if len(self.inventory.get_active_weapons()) <= self.cols:
                        for weapon in self.inventory.get_group('weapons').items:
                            if weapon.name == self.info.name:
                                weapon.add_active()
                                return
                        
 
                                
                    
                            
        
    
                           
    def render(self, surf):
        self.draw_ui(surf)
        if self.info:
            self.draw_info(self.info, surf, (self.base_pos[0] + 110, self.base_pos[1]))
            
            
        
        
                
        