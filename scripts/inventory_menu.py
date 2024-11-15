import pygame

from .config import config


class InventoryMenu:
    def __init__(self, game, inventory):
        self.game = game
        self.inventory = inventory
        self.size = 25 # size of each box
        self.config = config['items']
        
        self.item_boxes = []
        self.item_info = []
        
        

    def draw_ui(self, surf): # put each category of items into individual methods and then call all methods in this method 
        base_pos = [60, 20]
        
        all_boxes = [] # contains another array with [rect, name of item]
        # weapon boxes
        for i in range(4):
            rect = pygame.Rect(base_pos[0] + i * self.size, base_pos[1], self.size, self.size)
            pygame.draw.rect(surf, (255, 255, 255), rect, 1)
            weapons = list(self.game.assets.weapons.keys())
            for ix, weapon in enumerate(self.inventory.get_active_weapons()):
                if i == ix and weapon.name in weapons:
                    weapon_img = self.game.assets.weapons[weapon.name]
                    surf.blit(weapon_img, (rect.centerx - weapon_img.get_width() // 2 - 2, rect.centery - weapon_img.get_height() // 2 ))
                    all_boxes.append([rect, weapon.name])
        
        # item boxes
        for i in range(4):
            item_pos = [base_pos[0], 60]
            for j in range(4):
                rect = pygame.Rect(item_pos[0] + j * self.size, item_pos[1] + i * self.size, self.size, self.size)
                pygame.draw.rect(surf, (255, 255, 255), rect, 1)
                all_boxes.append([rect, ''])
            item_pos[1] += self.size
            
        return all_boxes
    
    def update(self):
        for box in self.item_boxes:
            if box[0].collidepoint(self.game.input.mpos): 
                if box[1]: # just a check to prevent crash since item boxes dont have a name yet 
                    if self.item_info and self.item_info[0][0] != box[1]: # if there already exists a name and description and the box you collide with is different
                        self.item_info.pop()
                    self.item_info.append([self.config[box[1]]['name'], self.config[box[1]]['description']])
                else:
                    self.item_info = []
                    
                
                        
    
    def render(self, surf):
        self.item_boxes = self.draw_ui(surf)
        if self.item_info:
            self.game.assets.fonts['small_white'].render(self.item_info[0][0], surf, (170, 25)) # name
            self.game.assets.fonts['small_white'].render(self.item_info[0][1], surf, (170, 45)) # description
        
        
                
        