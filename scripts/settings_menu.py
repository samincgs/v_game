import pygame
from scripts.const import SETTINGS

SETTINGS_OPTIONS = ['Display', 'Audio', 'Input', 'Quit']
SETTINGS_MENU_TYPES = ['main', 'display', 'audio', 'input']
SETTINGS_OPTIONS_GAP = 2

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.menu_cursor = 0
        self.menu = 'main'
        self.prev_menu = 'main'
    
    def reset(self):
        self.menu_cursor = 0
        self.menu = 'main'
        self.prev_menu = 'main'
    
    def change_menu(self, menu_type):
        self.prev_menu = self.menu
        self.menu = menu_type
    
    def update_render(self, surf):        
        mpos = self.game.input.mpos
        font = self.game.assets.fonts['small_white']
            
        # settings categories
        if self.menu == 'main':
            for idx, option in enumerate(SETTINGS_OPTIONS):
                loc = (20, 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP))
                option_rect = pygame.Rect(loc[0], loc[1], font.get_width(SETTINGS_OPTIONS[idx]), font.get_height())
                if option_rect.collidepoint(mpos):
                    self.menu_cursor = idx
                    if self.game.input.clicking('click'):
                        option_chosen = SETTINGS_OPTIONS[self.menu_cursor]
                        if option_chosen == 'Display':
                            self.change_menu('display')
                        elif option_chosen == 'Audio':
                            self.change_menu('audio')
                        elif option_chosen == 'Input':
                            self.change_menu('input')
                        elif option_chosen == 'Quit':
                            self.game.window.quit_window()
                        self.menu_cursor = 0
                font.outline_text(surf, option, (20, 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP)))
            
        # choosing the settings
        
                
        # displaying each submenu
        skip_cursor = False
        if self.menu != 'main':
            submenu_items = [(option, content) for option, content in SETTINGS.items() if content['submenu'] in (self.menu, 'all')]
            for idx, (option, content) in enumerate(submenu_items):
                loc = (20, 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP))
                option_rect = pygame.Rect(loc[0], loc[1], font.get_width(content['title']), font.get_height())
                if option_rect.collidepoint(mpos):
                    self.menu_cursor = idx
                    if self.game.input.clicking('click'):
                        if content['title'] == 'Show FPS':
                            self.game.window.show_fps = not self.game.window.show_fps
                        if content['title'] == 'Back':
                            self.menu_cursor = 0
                            self.change_menu(self.prev_menu)
                            skip_cursor = True
                font.outline_text(surf, content['title'], (20, 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP)))
                if content['title'] != 'Back':
                    font.outline_text(surf, ':',  (20 + font.get_width(content['title']), 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP)))
                if content['options']:
                    font.outline_text(surf, content['options'][0], (20 + font.get_width(content['title']) + 12, 20 + idx * (font.get_height() * SETTINGS_OPTIONS_GAP)))
        
        if not skip_cursor:   
            points = [
                (10, 20 + self.menu_cursor * (font.get_height() * SETTINGS_OPTIONS_GAP)),
                (13, 23 + self.menu_cursor * (font.get_height() * SETTINGS_OPTIONS_GAP)),
                (10, 26 + self.menu_cursor * (font.get_height() * SETTINGS_OPTIONS_GAP))
            ]
            
            pygame.draw.polygon(surf, (255, 255, 255), points=points)