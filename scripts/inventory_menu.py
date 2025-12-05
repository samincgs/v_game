import pygame

import scripts.pgtools as pt

from scripts.config import config

INVENTORY_LAYOUT = {
    'active': {
        'pos': [(0, 15), (50, 15), (60, 5), (60, -1), (0, -1)],
        'selected_pos': [(0, 20), (50, 20), (60, 10), (60, -1), (0, -1)]
    },
    'skills': {
        'pos': [(58, 15), (108, 15), (118, 5), (118, -1), (58, -1)],
        'selected_pos': [(58, 20), (108, 20), (118, 10), (118, -1), (58, -1)]
    },
    'items': {
        'pos': [(116, 15), (166, 15), (176, 5), (176, -1), (116, -1)],
        'selected_pos': [(116, 20), (166, 20), (176, 10), (176, -1), (116, -1)]
    }
}

INVENTORY_CATEGORIES = list(INVENTORY_LAYOUT)
ITEM_STARTING_POS = [(15, 30), (175, 30), (165, 40), (5, 40)]
TAB_POINTS = [(85, 20), (165, 20), (155, 30), (75, 30)]
TAB_HEIGHT = 15

class InventoryMenu:
    def __init__(self, game, inventory):
        self.game = game
        self.inventory = inventory
        self.config = config['items']

        self.images = {}
        
        self.category_selection_index = 0
        self.item_index = 0
        self.options_index = 0
        self.show_equip_options = False
        self.category_selected = INVENTORY_CATEGORIES[self.category_selection_index]
        
        self.animation_speed = 0.1
        self.line_progress = 0
        
        
        # lerp positions
        self.current_positions = {}
        self.tab_offsets = [0, -30]
        
        for category in INVENTORY_LAYOUT:
            self.current_positions[category] = [list(point) for point in INVENTORY_LAYOUT[category]['pos']]
        
    def get_image(self, type):
        if 'item_' + type in self.images:
            return self.images['item_' + type]
        img = pt.utils.load_img('data/images/animations/item_' + type + '/idle/0.png')
        self.images['item_' + type] = img
        return self.images['item_' + type]
    
    def get_tabs(self, category, item):
        options = ['unequip', 'cancel']
        if item is None:
                return options
        if category == 'active':
            pass
        elif category == 'skills':
            options = ['equip', 'cancel']
        elif category == 'items':
            options = ['cancel']
            if item.is_weapon or item.is_consumeable:
                options.insert(0, 'equip')
        return options
    
    def reset(self):
        self.category_selection_index = 0
        self.item_index = 0
        self.options_index = 0
        self.show_equip_options = False
       
    def update(self):
        
        if self.game.input.pressing('inventory_toggle'):
            self.reset()
        
        if self.game.input.pressing('right'):
            self.category_selection_index  = (self.category_selection_index + 1) % len(INVENTORY_CATEGORIES)
            # self.game.input.pressing['right'] = False
            self.item_index = 0
            self.options_index = 0
            self.show_equip_options = False
        if self.game.input.pressing('left'):
            self.category_selection_index  = (self.category_selection_index - 1) % len(INVENTORY_CATEGORIES)
            # self.game.input.pressing['left'] = False
            self.item_index = 0
            self.options_index = 0
            self.show_equip_options = False
        
            
        self.category_selected = INVENTORY_CATEGORIES[self.category_selection_index]
        active_weapons = self.inventory.get_active_weapons()
        items = self.inventory.get_items()
        
               
        if not self.show_equip_options:
            if self.category_selected == 'active':
                if self.game.input.pressing('down'):
                    self.item_index  = (self.item_index + 1) % len(active_weapons)
                    # self.game.input.pressing('down') = False
                    self.options_index = 0
                if self.game.input.pressing('up'):
                    self.item_index  = (self.item_index - 1) % len(active_weapons)
                    # self.game.input.pressing('up') = False
                    self.options_index = 0
                if self.game.input.pressing('equip'):
                    self.show_equip_options = True
                    
            elif self.category_selected == 'skills':
                pass
            elif self.category_selected == 'items':
                if self.game.input.pressing('down'):
                    self.item_index  = (self.item_index + 1) % len(items)
                    # self.game.input.pressing('down') = False
                if self.game.input.pressing('up'):
                    self.item_index  = (self.item_index - 1) % len(items)
                    # self.game.input.pressing('up') = False
                if self.game.input.pressing('equip'):
                    self.show_equip_options = True
        else:
            if self.category_selected == 'active':
                current_weapon = active_weapons[self.item_index] if active_weapons else None
                if current_weapon:
                    tabs = self.get_tabs(self.category_selected, current_weapon)
                    if self.game.input.pressing('down'):
                        self.options_index  = (self.options_index + 1) % len(tabs)
                        # self.game.input.pressing('down') = False
                    if self.game.input.pressing('up'):
                        self.options_index  = (self.options_index - 1) % len(tabs)
                        # self.game.input.pressing('up') = False
                    if self.game.input.pressing('equip'):
                        selected = tabs[self.options_index]
                        if selected == 'cancel':
                            self.show_equip_options = False
                            self.tab_offsets = [0, -30]
                            self.options_index = 0
                        elif selected == 'unequip':
                            self.inventory.remove_active_weapon(current_weapon)
                            self.show_equip_options = False
                            self.game.world.player.selected_weapon = 0
                            self.item_index = 0
                            self.category_selection_index = 0
                            
            elif self.category_selected == 'skills':
                pass
            elif self.category_selected == 'items':
                current_item = items[self.item_index] if items else None
                if current_item:
                    tabs = self.get_tabs(self.category_selected, current_item)
                    if self.game.input.pressing('down'):
                        self.options_index  = (self.options_index + 1) % len(tabs)
                        # self.game.input.pressing('down') = False
                    if self.game.input.pressing('up'):
                        self.options_index  = (self.options_index - 1) % len(tabs)
                        # self.game.input.pressing('up') = False
                    if self.game.input.pressing('equip'):
                        selected = tabs[self.options_index]
                        if selected == 'cancel':
                            self.show_equip_options = False
                            self.tab_offsets = [0, -30]
                            self.options_index = 0
                        elif selected == 'equip':
                            self.inventory.add_active_weapon(current_item) # currently only weapon
                            self.show_equip_options = False
                            self.category_selection_index = 0

    def draw_categories(self, surf, color, points, category, text_loc):
        pygame.draw.polygon(surf, (0, 0, 1), points=points)
        pygame.draw.lines(surf, color, False, points=points, width=1)
        self.game.assets.fonts['small_white'].render(surf, category, text_loc)
        
    def draw_items(self, surf, points, item, selected=False, amt=None):
        name = self.config[item.name]['name']
        pygame.draw.polygon(surf, (0, 0, 0), points)
        if selected:
            pygame.draw.polygon(surf, (255, 255, 255), points, width=1)
        self.game.assets.fonts['small_white'].render(surf, name, (points[0][0] + 2, points[0][1] + 3))
        if amt and amt > 1:
            self.game.assets.fonts['small_white'].render(surf, 'x' + str(amt), (points[0][0] + self.game.assets.fonts['small_white'].get_width(name) + 6, points[0][1] + 3))
        
    def draw_item_description(self, surf, item):
        name = self.config[item.name]['name']
        desc = self.config[item.name]['description']
        
        img = self.get_image(item.name)
        pt.utils.outline(surf, img, (surf.get_width() // 2, 23))
        surf.blit(img, (surf.get_width() // 2, 23))
        
        line_start_x = surf.get_width() // 2 + img.get_width() + 10
        line_end_x = line_start_x + self.game.assets.fonts['small_white'].get_width(name) + 2
        
        self.line_progress += (line_end_x - self.line_progress) * self.animation_speed
        
        self.game.assets.fonts['small_black'].render(surf, name, (surf.get_width() // 2 + img.get_width() + 10 + 1, 23 + 1))
        self.game.assets.fonts['small_white'].render(surf, name, (surf.get_width() // 2 + img.get_width() + 10, 23))
        pygame.draw.line(surf, (255, 255, 255), (line_start_x, 31), (self.line_progress, 31))
        self.game.assets.fonts['small_white'].render(surf, desc, (surf.get_width() // 2 + 7, 43), line_width=160)
        
        
    def draw_tabs(self, surf, options, current_option, base_points):
        base_x, base_y = base_points[0]
        for i, option in enumerate(options):
            target_offset = 0 if current_option == i else -30
            
            current = self.tab_offsets[i]
            self.tab_offsets[i] = current + (target_offset - current) * self.animation_speed
            x_offset = self.tab_offsets[i]
            
            y_offset = 12 * i
            
            poly_points = [
            (base_x + point[0] + x_offset, base_y + point[1] + y_offset) for point in TAB_POINTS
        ]
            
            pygame.draw.polygon(surf, (0, 0, 0), poly_points)   
            
            if i == current_option:
                pygame.draw.polygon(surf, (255, 255, 255), poly_points, width=1)
                
            text_pos = (poly_points[0][0] + 2, poly_points[0][1] + 2)
            self.game.assets.fonts['small_white'].render(surf, str(option), text_pos)
     
    def render(self, surf):

        if self.category_selected == 'active':
            for i, weapon in enumerate(self.inventory.get_active_weapons()):
                selected = True if i == self.item_index else False
                extra_y = TAB_HEIGHT * len(self.get_tabs(self.category_selected, self.inventory.get_active_weapons()[self.item_index])) if self.show_equip_options and i > self.item_index else 0
                points = [(pos[0], pos[1] + i * 20 + extra_y) for pos in ITEM_STARTING_POS]
                self.draw_items(surf, points, weapon, selected=selected)
                if selected:
                    self.draw_item_description(surf, weapon)
                    if self.show_equip_options:
                        tabs = self.get_tabs(self.category_selected, self.inventory.get_active_weapons()[self.item_index])
                        self.draw_tabs(surf, tabs, self.options_index, base_points=points)
        elif self.category_selected == 'skills':
            pass
        elif self.category_selected == 'items':
            for i, item in enumerate(self.inventory.get_items()):
                selected = True if i == self.item_index else False
                extra_y = TAB_HEIGHT * len(self.get_tabs(self.category_selected, self.inventory.get_items()[self.item_index])) if self.show_equip_options and i > self.item_index else 0
                points = [(pos[0], pos[1] + i * 20 + extra_y) for pos in ITEM_STARTING_POS]
                self.draw_items(surf, points=points, item=item, amt=item.amount, selected=selected)
                if selected:
                    self.draw_item_description(surf, item)
                    if self.show_equip_options:
                        tabs = self.get_tabs(self.category_selected, self.inventory.get_items()[self.item_index])
                        self.draw_tabs(surf, tabs, self.options_index, base_points=points)
            
        for category in reversed(INVENTORY_CATEGORIES):
            if category == self.category_selected:
                color = (255, 255, 255)
                target_pos = INVENTORY_LAYOUT[category]['selected_pos']
            else:
                target_pos = INVENTORY_LAYOUT[category]['pos']
                color = (73, 80, 101)
                
            for i, target_point in enumerate(target_pos):
                current_point = self.current_positions[category][i]
                self.current_positions[category][i] = [current_point[0] + (target_point[0] - current_point[0]) * self.animation_speed, current_point[1] + (target_point[1] - current_point[1]) * self.animation_speed]
            
            pos = self.current_positions[category]
                
            self.draw_categories(surf, color, pos, category, (pos[0][0] + 6, pos[0][1] - 8))
        
        
        