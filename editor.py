import pygame
import sys
import tkinter as tk
from tkinter import filedialog

from scripts.tilemap import Tilemap
from scripts.asset import Asset
from scripts.font import Font

from scripts.config import config

class LevelEditor:
    def __init__(self, display_size, display_scale):
        self.display_size = display_size
        self.display_scale = display_scale
        
        pygame.init()
        pygame.display.set_caption('Level Editor')
        self.screen = pygame.display.set_mode((display_size[0] * display_scale, display_size[1] * display_scale))
        self.display = pygame.Surface(self.display_size)
        self.clock = pygame.time.Clock()
        
        self.file_name = None
        
        self.tilemap = Tilemap(self, 16, self.display_size)
        self.assets = Asset()
        self.font = Font('data/fonts/small_font.png', (208, 223, 215))
        self.config = config['autotile']
        
        self.scroll = [0, 0]
        self.scroll_speed = 2
        self.movement = [False, False, False, False]
        
        self.clicking = False
        self.right_clicking = False
        self.click = False
        self.right_click = False
        
        self.tile_list = list(self.assets.tiles)
        self.tile_group = 0
        self.tile_variant = 0
        self.selected_group = self.tile_list[0]
        self.layer_opacity = False
        self.sidebar_size = 130
        self.sidebar_color = (20, 36, 50)
        self.sidebar_rect_color = (33, 57, 78)
        self.selection_points = []
        self.selection_rect = None
        
        self.placement_mode = 'grid'
        self.current_layer = "0"
    
    def autotile(self, curr_layer):
        # if self.selection_rect: # only with rect
            for layer in self.tilemap.tilemap:
                if curr_layer == layer:
                    for str_tile in self.tilemap.tilemap[layer]:
                            tile = self.tilemap.tilemap[layer][str_tile]
                            neighbours = []
                            for offset in self.config['check_offsets']:
                                tile_loc = (tile['pos'][0] + offset[0], tile['pos'][1] + offset[1])
                                # if not self.selection_rect.collidepoint((tile_loc[0] * self.tilemap.tile_size, tile_loc[1] * self.tilemap.tile_size)):  # only with rect
                                #     continue  
                                str_loc = str(tile_loc[0]) + ';' + str(tile_loc[1])
                                if str_loc in self.tilemap.tilemap[layer]:
                                    if tile['type'] == self.tilemap.tilemap[layer][str_loc]['type']:
                                        neighbours.append(offset)
                            neighbours = sorted(neighbours)
                            for border in self.config['tile_borders']:
                                replacement_tile = border['tile']
                                border_list = sorted(border['border_list'])
                                if neighbours == border_list:
                                    tile['variant'] = replacement_tile
        
        # self.selection_rect = None # only with rect
        # self.selection_points = [] # only with rect
            
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            # camera
            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_speed
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_speed
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # mouse pos
            mpos = pygame.mouse.get_pos()
            mpos = (int(mpos[0] / self.display_scale), int(mpos[1] / self.display_scale))
            scaled_mpos = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])
            tile_pos = (int(mpos[0] + self.scroll[0]) // self.tilemap.tile_size, int(mpos[1] + self.scroll[1]) // self.tilemap.tile_size)
            
            current_tile = self.assets.tiles[self.tile_list[self.tile_group]][self.tile_variant].copy()
            tile_choice = current_tile.copy()
            tile_choice.set_alpha(210)
                        
            if mpos[0] > self.sidebar_size:
                if self.placement_mode == 'grid':
                    tile_data = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos }
                    if self.clicking:
                        self.tilemap.add_tile(tile_data, self.current_layer)
                    elif self.right_clicking:
                        self.tilemap.remove_tile(tile_data, self.current_layer)
                        # remove grid tile
                else: # offgrid
                    tile_data = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': scaled_mpos }
                    if self.click:
                        self.tilemap.add_offgrid_tile(tile_data, self.current_layer)
                    elif self.right_click:
                        self.tilemap.remove_offgrid_tile(self.current_layer, curr_mpos=scaled_mpos)
                                
                                
            # draw topleft sidebar  
            sidebar_surf = pygame.Surface((self.sidebar_size, 100))
            sidebar_surf.fill(self.sidebar_color)
            pygame.draw.rect(sidebar_surf, self.sidebar_rect_color, pygame.Rect(-1, -1, sidebar_surf.get_width() + 1, sidebar_surf.get_height() + 1), 1)
            
            # SELECT TYPE OF TILE GROUP (TOP HALF)
            for ix, val in enumerate(self.tile_list):
                offset_x = 0
                tile_sheet = pygame.Rect(1, 2 + ix * 11, self.sidebar_size, 10)
                if tile_sheet.collidepoint(mpos):
                    if self.clicking:
                        self.tile_variant = 0
                        self.selected_group = val
                        self.tile_group = self.tile_list.index(self.selected_group)
                    offset_x = 2
                self.font.render(str(val), sidebar_surf, (1 + offset_x, 2 + ix * 11))
            
            # draw bottom left sidebar
            tile_selector_surf = pygame.Surface((sidebar_surf.get_width(), self.display_size[1] - sidebar_surf.get_height()))
            tile_selector_surf.fill(self.sidebar_color)
            pygame.draw.line(tile_selector_surf, self.sidebar_rect_color, (tile_selector_surf.get_width() - 1, 0), (tile_selector_surf.get_width() - 1, tile_selector_surf.get_height() - 1))
            
            # SELECT TILES (BOTTOM HALF)
            for ix, val in enumerate(self.assets.tiles[self.tile_list[self.tile_group]]):
                y_offset = 0
                tile_rect = pygame.Rect(1, sidebar_surf.get_height() + 1 + (20 * ix), val.get_width(), val.get_height())
                if tile_rect.collidepoint(mpos):
                    if self.clicking:
                        self.tile_variant = ix
                    y_offset = 2
                tile_selector_surf.blit(val, (1, 1 + (20 * ix) - y_offset))
            
            self.tilemap.render_editor(self.current_layer, self.layer_opacity, self.display, offset=render_scroll)
            
            if self.placement_mode == 'grid':
                self.display.blit(tile_choice, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(tile_choice, mpos)
            
            self.display.blit(current_tile, (self.sidebar_size + 20, 20))
            
            self.font.render('file: ' + (str(self.file_name.split('/')[-1]) if self.file_name else 'None'), self.display, ((self.display.get_width() - 70 if self.file_name else self.display.get_width() - 53), 5))
            self.font.render('placement_mode: ' + str(self.placement_mode), self.display, (self.display.get_width() - 98, 20))
            self.font.render('layer: ' + str(self.current_layer), self.display, (self.display.get_width() - 46, 35))
            self.font.render('pos: ' + str(list(tile_pos) if self.placement_mode == 'grid' else list(scaled_mpos)), self.display, (self.display.get_width() - 60, 50))
            
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
                        if self.file_name:
                            self.tilemap.write_map(self.file_name)
                        else:
                            file = filedialog.asksaveasfile(title='Save Map', filetypes=[('json files', '*.json'), ('all files', "*.*")])
                            if file:
                                self.tilemap.write_map(file.name)
                                self.file_name = file.name              
                    if event.key == pygame.K_i:
                        root = tk.Tk()
                        root.withdraw()
                        self.file_name = filedialog.askopenfilename(title='Select Map', filetypes=[('json files', '*.json'), ('all files', "*.*")])
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
                        self.autotile(self.current_layer)
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
                        self.current_layer = int(self.current_layer) + 1
                        self.current_layer = str(self.current_layer)
                    if event.button == 5:
                        self.current_layer = int(self.current_layer) - 1
                        self.current_layer = str(self.current_layer)
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
    LevelEditor((600, 400), 2).run()
            