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
    