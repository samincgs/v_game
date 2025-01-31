import pygame

def load_image(path, colorkey=(0, 0, 0), alpha=False):
    img = pygame.image.load(path).convert() if not alpha else pygame.image.load(path).convert_alpha()
    img.set_colorkey(colorkey)
    return img

def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_rect)
    img = surf.subsurface(handle_surf.get_clip())
    return img.copy()

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
    
        

        
