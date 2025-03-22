import pygame

import pygame
import os
import json

# load pygame image
def load_img(path, colorkey=(0, 0, 0), alpha=False):
    img = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
    if colorkey:
        img.set_colorkey(colorkey)
    return img

# load a directory of imgs in a list
def load_imgs(path, colorkey=(0, 0, 0), alpha=False):
    tiles = []
    for file in sorted(os.listdir(path)):
        img = load_img(path + '/' + file, colorkey=colorkey, alpha=True)
        tiles.append(img)
    return tiles

# load a directory of images into a dictionary
def load_dir(path, colorkey=(0, 0, 0), alpha=False):
    tiles = {}
    for file in sorted(os.listdir(path)):
        name = file.split('.')[0]
        img = load_img(path + '/' + file, colorkey=colorkey, alpha=alpha)
        tiles[name] = img
    return tiles

# load multiple directories into a dict with lists of images
def load_dir_list(path, colorkey=(0, 0, 0), alpha=False):
    image_dir = {}
    for folder in sorted(os.listdir(path)):
        image_dir[folder] = []
        for img in os.listdir(path + '/' + folder):
            image_dir[folder].append(load_img(os.path.join(path, folder, img), colorkey, alpha))                                       
    return image_dir

# load all sound files from a dict into a dict
def load_sounds(path):
    tiles = {}
    for file in sorted(os.listdir(path)):
        name = file.split('.')[0]
        sound = pygame.mixer.Sound(path + '/' + file)
        tiles[name] = sound
    return tiles

# load a json file and return its data
def load_json(path):
    f = open(path)
    map_data = json.load(fp=f)
    f.close()
    return map_data

# open a file and save data into the file
def save_json(path, data):
    f = open(path, 'w')
    json.dump(data, fp=f)
    f.close()

# load a text file into a 2D list of numbers (can be string or int)
def load_map_txt(path, ints=False):
    map = []
    data = read_file(path)
    data = data.split('\n')
    for row in data:
        if not ints:
            map.append(row.split())
        else:
           map.append([int(num) for num in row.split()])
    return map

# read a text file
def read_file(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

# create a smaller subsurface of a bigger surface
def clip(surf, loc, size):
    main_surf = surf.copy()
    clipped_rect = pygame.Rect(loc[0], loc[1], size[0], size[1])
    main_surf.set_clip(clipped_rect)
    img = main_surf.subsurface(main_surf.get_clip())
    return img.copy()

# do a color swap, between an old and new color
def palette_swap(img, old_color, new_color):
    handle_img = img.copy()
    handle_img.fill(new_color)
    img.set_colorkey(old_color)
    handle_img.blit(img, (0, 0))
    return handle_img 

def outline(surf, img, loc, color=(255, 255, 255)):
    mask_img = pygame.mask.from_surface(img)
    mask_img = mask_img.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
    for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        surf.blit(mask_img, (loc[0] + offset[0], loc[1] + offset[1]))

def normalize(value, amt, target=0):
    if (value + amt) < target:
        value += amt
    elif (value - amt) > target:
        value -= amt
    else:
        value = target
    return value

def blit_center(surf, img, pos):
    surf.blit(img, (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2))
    
def glow(surf, pos, radius, color):
    circle_surf = pygame.Surface((radius * 2, radius * 2))
    circle_surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(circle_surf, color, (radius, radius), radius)
    surf.blit(circle_surf, (pos[0] - radius, pos[1] - radius), special_flags=pygame.BLEND_RGB_ADD)
    
        

        
