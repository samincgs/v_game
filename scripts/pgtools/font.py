from .utils import clip, load_img, palette_swap

class Font:
    def __init__(self, path='data/fonts/main_font.png', font_color=(255, 255, 255)):
        self.font_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '/', '\\', '-', '\'', ',', ']','[', '_', ':', '%', '?']
        self.font_sheet = load_img(path, colorkey=(0, 0, 0))
        self.font_color = font_color
        if font_color != (255, 255, 255):
            self.font_sheet = palette_swap(self.font_sheet, (255, 255, 255), font_color)
            
        self.characters = {}
        self.count = 0
        self.current_width = 0
        self.spacing = 1

        for x in range(self.font_sheet.get_width()):
            if self.font_sheet.get_at((x, 0))[0] == 127:
                char_img = clip(self.font_sheet, (x - self.current_width, 0), (self.current_width, self.font_sheet.get_height()))
                self.characters[self.font_order[self.count]] = char_img.copy()
                self.count += 1
                self.current_width = 0
            else:
                self.current_width += 1
            x += 1 
            
        self.base_size = self.characters['a'].get_size()
        
    def get_width(self, text):
        width = 0
        for char in text:
            if char not in [' ', '\n']:
                width += self.characters[char].get_width() + self.spacing
            elif char == ' ':
                width += self.base_size[0]
        return width
    
    def get_height(self):
        return self.base_size[1]
    
    def outline_text(self, surf, text, loc, outline_color, spacing=(1, 1)):
        outline_font = Font(font_color=outline_color)
        outline_font.render(surf, text, (loc[0] + spacing[0], loc[1] + spacing[1]))
        self.render(surf, text, loc)
        
    def render(self, surf, text, loc, line_width=0):
        
        if line_width: # add line width and modify text before rendering
            curr_width = 0
            spaced_text = text.split(' ')
            for i, word in enumerate(spaced_text):
                w = self.get_width(word)
                if curr_width + w > line_width:
                    spaced_text[i] = '\n' + word
                    curr_width = w
                else:
                    curr_width += w
            text = ' '.join(spaced_text)
        
        x_offset = 0
        loc = list(loc)
        for char in text:
            if char not in [' ', '\n']:
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            elif char == ' ':
                x_offset += self.base_size[0]
            elif char == '\n':
                x_offset = 0
                loc[1] += self.base_size[1] * 2
    
                
