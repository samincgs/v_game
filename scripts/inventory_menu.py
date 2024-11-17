import pygame

from .config import config


class InventoryMenu:
    def __init__(self, game, inventory):
        self.game = game
        self.inventory = inventory
        self.size = 25 # size of each box
        self.config = config['items']
        
        self.base_pos = [60, 40]
        self.color = (187, 196, 204)
        self.item_boxes = [] # [[rect of box, weapon/item name]]
        self.item_info = [] # [[item name (from config), item description, weapon/item name (weapon type), item_type]]
        
        

    def draw_ui(self, surf):  # TODO: CHANGE COLOR of empty boxes
        
        all_boxes = [] # contains another array with [rect, name of item] -> self.item_boxes
        # weapon boxes
        for i in range(4):
            rect = pygame.Rect(self.base_pos[0] + i * self.size, self.base_pos[1], self.size, self.size)
            color = (124, 140, 156)
            for ix, weapon in enumerate(self.inventory.get_active_weapons()):
                if ix == i:
                    weapon_img = self.game.assets.weapons[weapon.name]
                    color = (255, 255, 255)
                    surf.blit(weapon_img, (rect.centerx - weapon_img.get_width() // 2 - 2, rect.centery - weapon_img.get_height() // 2 ))
                    all_boxes.append([rect, weapon.name])
            
            pygame.draw.rect(surf, color, rect, 1)
        
        # item boxes
        for i in range(4):
            item_pos = [self.base_pos[0], self.base_pos[1] + 40]
            for j in range(4):
                color = (124, 140, 156)
                rect = pygame.Rect(item_pos[0] + j * self.size, item_pos[1] + i * self.size, self.size, self.size)
                for ix, item in enumerate(self.inventory.get_items()):
                    if ix == j + i * 4:
                        color = (255, 255, 255)
                        item_img = self.game.assets.weapons[item.name] if item.type == 'weapon' else self.game.assets.items[item.name]
                        surf.blit(item_img, (rect.centerx - item_img.get_width() // 2, rect.centery - item_img.get_height() // 2))
                        all_boxes.append([rect, item.name])
                    
                pygame.draw.rect(surf, color, rect, 1)
                
            item_pos[1] += self.size
            
        return all_boxes
    
    def draw_item_label(self, item_info, surf, loc):
        img = self.game.assets.weapons[item_info[0][2]] if item_info[0][3] == 'weapon' else self.game.assets.items[item_info[0][2]]
        surf.blit(img, loc)
        self.game.assets.fonts['small_white'].render(item_info[0][0], surf, (loc[0] + img.get_width() + 5, loc[1])) # name
        self.game.assets.fonts['small_white'].render(item_info[0][1], surf, (loc[0], loc[1] + 20)) # description
    
    
    def update(self):
        self.item_info = []
        for box in self.item_boxes:
            if box[0].collidepoint(self.game.input.mpos): 
                self.item_info.append([self.config[box[1]]['name'], self.config[box[1]]['description'], box[1], self.config[box[1]]['type']])
                if self.game.input.mouse_states['shoot']:
                    for item in self.inventory.get_items():
                        if item.type == 'weapon' and item.name == self.item_info[0][2]:
                            item.add_active()
                
                
            
    def render(self, surf):
        self.item_boxes = self.draw_ui(surf)
        if self.item_info:
            self.draw_item_label(self.item_info, surf, (170, self.base_pos[1]))
            
        
        
                
        