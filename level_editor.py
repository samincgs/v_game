import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog

from scripts.tilemap import Tilemap
from scripts.font import Font
from scripts.utils import load_json

class LevelEditor:
    def __init__(self):
        pygame.init()
        
        self.config = load_json('data/images/spritesheets/config.json')
        self.display_size = (600, 400)
        self.display_scale = 2
        
        pygame.display.set_caption('Level Editor')
        self.screen = pygame.display.set_mode((self.display_size[0] * self.display_scale, self.display_size[1] * self.display_scale))
        self.display = pygame.Surface(self.display_size)
        self.clock = pygame.time.Clock() 
                
        self.file_name = None
        
        self.tilemap = Tilemap(self, tile_size=self.config['tile_size'])
        self.spritesheet_data = self.tilemap.load_spritesheets('data/images/spritesheets/')
        
        
        self.font = Font('data/fonts/main_font.png', (208, 223, 215))
        
        self.scroll = [0, 0]
        self.sidebar_scroll = [0, 0]
        self.scroll_speed = 4
        self.movement = [False, False, False, False]
        
        self.clicking = False
        self.right_clicking = False
        self.click = False
        self.right_click = False
        self.scrolled_up = False
        self.scrolled_down = False
        
        self.tile_list = list(self.spritesheet_data)
        self.tile_group = 0
        self.tile_variant = 0
        self.selected_group = self.tile_list[0]
        self.layer_opacity = False
        self.sidebar_size = 100
        self.sidebar_color = (20, 36, 50)
        self.sidebar_rect_color = (33, 57, 78)
        self.selection_points = []
        self.selection_rect = None
        
        self.placement_mode = 'grid'
        self.current_layer = '0'
    
    def reset_rect(self):
        self.selection_rect = None # only with rect
        self.selection_points = [] # only with rect
    
    def autotile(self): # keybinding: t
        
        if self.selection_rect: # only with rect
            for loc in self.tilemap.tilemap:
                for layer in (int(layer) for layer in self.tilemap.tilemap[loc]):
                    layer = str(layer)
                    if self.current_layer == layer:
                        layer = str(layer)
                        tile = self.tilemap.tilemap[loc][layer]
                        neighbours = []
                        for offset in self.config['check_offsets']:
                            tile_loc = (tile['tile_pos'][0] + offset[0], tile['tile_pos'][1] + offset[1])
                            if not self.selection_rect.collidepoint((tile_loc[0] * self.tilemap.tile_size, tile_loc[1] * self.tilemap.tile_size)):  # only with rect
                                continue  
                            str_loc = str(tile_loc[0]) + ';' + str(tile_loc[1])
                            if str_loc in self.tilemap.tilemap:
                                if layer in self.tilemap.tilemap[str_loc]:
                                    if tile['type'] == self.tilemap.tilemap[str_loc][layer]['type'] and tile['type'] in self.config['autotile_types']:
                                        neighbours.append(offset)
                        neighbours = sorted(neighbours)
                        for border in self.config['tile_borders']:
                            replacement_tile = border['tile']
                            border_list = sorted(border['border_list'])
                            if neighbours == border_list:
                                tile['variant'] = replacement_tile
                                    
        self.reset_rect()
    
    def remove_all_tiles(self): # keybinding: x
        
        if self.selection_rect: # only with rect
            for loc in self.tilemap.tilemap:
                for layer in self.tilemap.tilemap[loc].copy():
                    if self.current_layer == layer:
                        tile = self.tilemap.tilemap[loc][layer]
                        if self.selection_rect.collidepoint((tile['tile_pos'][0] * self.tilemap.tile_size, tile['tile_pos'][1] * self.tilemap.tile_size)):  # only with rect
                            del self.tilemap.tilemap[loc][layer]
        
        self.reset_rect()
        
    def floodfill(self, curr_pos):
        floodfill_list = [curr_pos]
        visited = set()
        
        while floodfill_list:
            tile = floodfill_list.pop(0)
            
            if tuple(tile) in visited:
                continue
            
            
            visited.add(tuple(tile))
                
            scaled_mpos = (tile[0] + self.scroll[0] * self.tilemap.tile_size, tile[1] + self.scroll[1] * self.tilemap.tile_size)
            tile_data = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': scaled_mpos, 'tile_pos': tuple(tile), 'layer': self.current_layer }
            self.tilemap.add_tile(tile_data)
            
            bordering_tiles = [[tile[0] + 1, tile[1]], [tile[0] - 1, tile[1]], [tile[0], tile[1] + 1], [tile[0], tile[1] - 1]]
            for b in bordering_tiles:
                if not self.tilemap.get_tile(b) and tuple(b) not in visited:
                    floodfill_list.append(b)
            
            print(f"Floodfill List: {floodfill_list}")
       
    
    def render_editor(self, surf, offset=(0,0)): 
        
        render_queue = []

        for layer in sorted(int(layer) for layer in self.tilemap.offgrid_tiles):
            tile_layer = self.tilemap.offgrid_tiles[str(layer)]
            for tile in tile_layer:
                if not self.layer_opacity:
                    img = self.spritesheet_data[tile['type']][tile['variant']]
                    render_queue.append((int(layer), img.copy(), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
                else:
                    if self.current_layer == str(layer):
                        img = self.spritesheet_data[tile['type']][tile['variant']].copy()
                        render_queue.append((int(layer), img.copy(), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
                    else:
                        img = self.spritesheet_data[tile['type']][tile['variant']].copy()
                        img.set_alpha(75)
                        render_queue.append((int(layer), img.copy(), (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1])))
        
        for loc in self.tilemap.tilemap:
            for layer in sorted(int(layer) for layer in self.tilemap.tilemap[loc]):
                tile = self.tilemap.tilemap[loc][str(layer)]
                if not self.layer_opacity:
                    img = self.spritesheet_data[tile['type']][tile['variant']]
                    render_queue.append((int(layer), img.copy(), (tile['tile_pos'][0] * self.tilemap.tile_size - offset[0], tile['tile_pos'][1] * self.tilemap.tile_size - offset[1])))
                else:
                    if self.current_layer == str(layer):
                        img = self.spritesheet_data[tile['type']][tile['variant']]
                        render_queue.append((int(layer), img.copy(), (tile['tile_pos'][0] * self.tilemap.tile_size - offset[0], tile['tile_pos'][1] * self.tilemap.tile_size - offset[1])))
                    else:
                        img = self.spritesheet_data[tile['type']][tile['variant']].copy()
                        img.set_alpha(75)
                        render_queue.append((int(layer), img.copy(), (tile['tile_pos'][0] * self.tilemap.tile_size - offset[0], tile['tile_pos'][1] * self.tilemap.tile_size - offset[1])))
        
        
        render_queue.sort(key=lambda x: x[0]) # sort the layer
        
        for tile in render_queue:
            surf.blit(tile[1], tile[2])
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            # camera
            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_speed
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_speed
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # mouse pos
            mpos = pygame.mouse.get_pos()
            mpos = (int(mpos[0] // self.display_scale), int(mpos[1] // self.display_scale))
            scaled_mpos = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
            tile_pos = (int(mpos[0] + self.scroll[0]) // self.tilemap.tile_size, int(mpos[1] + self.scroll[1]) // self.tilemap.tile_size)
                        
            current_tile = self.spritesheet_data[self.tile_list[self.tile_group]][self.tile_variant].copy()
            tile_choice = current_tile.copy()
            tile_choice.set_alpha(210)
                        
            if mpos[0] > self.sidebar_size:
                if self.placement_mode == 'grid':
                    tile_data = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': scaled_mpos, 'tile_pos': tile_pos, 'layer': self.current_layer }
                    if self.clicking:
                        self.tilemap.add_tile(tile_data)
                    elif self.right_clicking:
                        self.tilemap.remove_tile(tile_data)
                        # remove grid tile
                else: # offgrid
                    tile_data = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': scaled_mpos, 'tile_pos': tile_pos, 'layer': self.current_layer }
                    if self.click:
                        self.tilemap.add_offgrid_tile(tile_data)
                    elif self.right_click:
                        self.tilemap.remove_offgrid_tile(self.current_layer, curr_mpos=scaled_mpos)
                                
                                
            # draw topleft sidebar  
            sidebar_surf = pygame.Surface((self.sidebar_size, 100))
            sidebar_surf.fill(self.sidebar_color)
            pygame.draw.rect(sidebar_surf, self.sidebar_rect_color, pygame.Rect(-1, -1, sidebar_surf.get_width() + 1, sidebar_surf.get_height() + 1), 1)
            
            # SELECT TYPE OF TILE GROUP (TOP HALF)
            for ix, val in enumerate(self.tile_list):
                offset_x = 0
                tile_h = 2 + ix * 11 - self.sidebar_scroll[0]
                tile_sheet = pygame.Rect(1, tile_h, self.sidebar_size, 10)
                if tile_sheet.collidepoint(mpos):
                    if self.clicking:
                        self.tile_variant = 0
                        self.selected_group = val
                        self.tile_group = self.tile_list.index(self.selected_group)
                    offset_x = 2
                self.font.render(sidebar_surf, str(val), (1 + offset_x, tile_h))
            
            # draw bottom left sidebar
            tile_selector_surf = pygame.Surface((sidebar_surf.get_width(), self.display_size[1] - sidebar_surf.get_height()))
            tile_selector_surf.fill(self.sidebar_color)
            pygame.draw.line(tile_selector_surf, self.sidebar_rect_color, (tile_selector_surf.get_width() - 1, 0), (tile_selector_surf.get_width() - 1, tile_selector_surf.get_height() - 1))
            
            # SELECT TILES (BOTTOM HALF)
            max_height = max([tile.get_height() for tile in self.spritesheet_data[self.tile_list[self.tile_group]]])
            for ix, val in enumerate(self.spritesheet_data[self.tile_list[self.tile_group]]): 
                y_offset = 0
                tile_h = sidebar_surf.get_height() + 2 + (max_height * ix * 1.5) + self.sidebar_scroll[1]
                tile_rect = pygame.Rect(1, tile_h, val.get_width(), val.get_height())
                if tile_rect.collidepoint(mpos):
                    if self.clicking:
                        self.tile_variant = ix
                    y_offset = 2
                tile_selector_surf.blit(val, (1, 2 + (max_height * ix * 1.5) - y_offset + self.sidebar_scroll[1]))
            
            self.render_editor(self.display, offset=render_scroll)
            
            if self.placement_mode == 'grid':
                self.display.blit(tile_choice, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(tile_choice, mpos)
            
            self.display.blit(current_tile, (self.sidebar_size + 20, 20))
            
            right_offset = 5
            y_text_pos = 7
            
            file_text = 'file: ' + (str(self.file_name.split('/')[-1]) if self.file_name else 'None')
            self.font.render(self.display, file_text, (self.display.get_width() - self.font.width(file_text) - right_offset, y_text_pos))
            y_text_pos += 15
            
            placement_text = 'placement_mode: ' + str(self.placement_mode)
            self.font.render(self.display, placement_text, (self.display.get_width() - self.font.width(placement_text) - right_offset, y_text_pos))
            y_text_pos += 15
            
            layer_text = 'layer: ' + str(self.current_layer)
            self.font.render(self.display, layer_text, (self.display.get_width() - self.font.width(layer_text) - right_offset, y_text_pos))
            y_text_pos += 15
            
            pos_text = 'pos: ' + str(list(scaled_mpos))
            self.font.render(self.display, pos_text, (self.display.get_width() - self.font.width(pos_text) - right_offset, y_text_pos))
            y_text_pos += 15
            
            tile_pos_text = 'tile_pos: ' + str(list(tile_pos))
            self.font.render(self.display, tile_pos_text, (self.display.get_width() - self.font.width(tile_pos_text) - right_offset, y_text_pos))
            y_text_pos += 15
            
            
            if mpos[0] < self.sidebar_size:
                if mpos[1] < 100:
                    if len(self.tile_list) > 10:
                        if self.scrolled_up and self.sidebar_scroll[0] > 0:
                            self.sidebar_scroll[0] -= 10
                        if self.scrolled_down :
                            self.sidebar_scroll[0] += 10
                else:
                    if self.scrolled_up and self.sidebar_scroll[1] > 0:
                        self.sidebar_scroll[1] -= 10
                    if self.scrolled_down:
                        self.sidebar_scroll[1] += 10
            
            if len(self.selection_points):
                start_point = self.selection_points[0]
                if self.selection_points[1] != None:
                    end_point = self.selection_points[1]
                    if end_point[0] > start_point[0]:
                        self.selection_rect = pygame.Rect(start_point[0], start_point[1], (end_point[0] - start_point[0]), (end_point[1] - start_point[1]))
                    else:
                        self.selection_rect = pygame.Rect(end_point[0], end_point[1], (start_point[0] - end_point[0]), (start_point[1] - end_point[1]))

                    displayed_rect = self.selection_rect.copy()
                    displayed_rect.x -= self.scroll[0]
                    displayed_rect.y -= self.scroll[1]
                    if self.selection_points[2] != True:
                        pygame.draw.rect(self.display, (0, 0, 152), displayed_rect, 1)
                    else:
                        self.selection_points = []
                        self.selection_rect = None
                        
                    
                
            self.click = False
            self.right_click = False
            self.scrolled_up = False
            self.scrolled_down = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.placement_mode = 'offgrid' if self.placement_mode == 'grid' else 'grid'
                    if event.key == pygame.K_l:
                        self.layer_opacity = not self.layer_opacity
                    if event.key == pygame.K_o:
                        root = tk.Tk()
                        root.withdraw()
                        current_file = self.file_name.split('/')[-1] if self.file_name else None
                        file = filedialog.asksaveasfile(initialfile=current_file, defaultextension='.json', title='Save Map', filetypes=[('json files', '*.json'), ('all files', "*.*")], initialdir=os.path.join(os.getcwd(), 'data', 'maps'))
                        if file:
                            self.tilemap.write_map(file.name)
                            self.file_name = file.name     
                            file.close()         
                    if event.key == pygame.K_i:
                        root = tk.Tk()
                        root.withdraw()
                        self.file_name = filedialog.askopenfilename(title='Select Map', filetypes=[('json files', '*.json'), ('all files', "*.*")], initialdir=os.path.join(os.getcwd(), 'data', 'maps'))
                        if self.file_name:
                            self.tilemap.load_map(self.file_name)
                    if event.key == pygame.K_e:
                        if not len(self.selection_points):
                            self.selection_points = [scaled_mpos, None, None]
                        elif self.selection_points[1] == None:
                            self.selection_points[1] = scaled_mpos
                        elif self.selection_points[2] == None:
                            self.selection_points[2] = True
                    if event.key == pygame.K_t:
                        self.autotile()
                    if event.key == pygame.K_x:
                        self.remove_all_tiles()
                    if event.key == pygame.K_f:
                        self.floodfill(tile_pos)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        self.click = True
                    if event.button == 3:
                        self.right_clicking = True
                        self.right_click = True
                    if event.button == 4:
                        self.scrolled_up = True
                        if mpos[0] > self.sidebar_size:
                            self.current_layer = str(int(self.current_layer) + 1)
                    if event.button == 5:
                        self.scrolled_down = True
                        if mpos[0] > self.sidebar_size:
                            self.current_layer = str(int(self.current_layer) - 1)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        
                        
            self.display.blit(sidebar_surf, (0, 0))
            self.display.blit(tile_selector_surf, (0, sidebar_surf.get_height()))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
if __name__ == '__main__':
    LevelEditor().run()
            