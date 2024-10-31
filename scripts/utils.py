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
    img.set_colorkey(old_color)
    handle_img = img.copy()
    handle_img.fill(new_color)
    handle_img.blit(img, (0, 0))
    return handle_img 

def outline(surf, img, loc, color=(255, 255, 255)):
    mask_img = pygame.mask.from_surface(img)
    mask_img = mask_img.to_surface(setcolor=color, unsetcolor=(255, 0, 255, 0))
    for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        surf.blit(mask_img, (loc[0] + offset[0], loc[1] + offset[1]))
    