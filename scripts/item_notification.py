from copy import deepcopy

class ItemNotification:
    def __init__(self, game):
        self.game = game
        self.item_data = [] # name, count, timer
        
        self.item_appear_time = 4
        
        self.transition = 0
        self.transition_speed = 300
        
    def add_item_notif(self, item):
        for item_info in self.item_data:
            if item_info[0] == item.name:
                    item_info[1] += item.amount
                    return
        self.item_data.append([item.name, 1, 0])
    
    def update(self, dt):
        
        
        for item_info in self.item_data.copy():
            item_info[2] += dt
            if item_info[2] > self.item_appear_time:
                self.transition = max(self.transition - dt * self.transition_speed, 0)
                if not self.transition:
                    self.item_data.remove(item_info)
            else:
                self.transition = min(self.transition + dt * self.transition_speed, 60)
            
                
            
    def render(self, surf):
        height = 20 
        for idx, item_info in enumerate(reversed(self.item_data.copy())):
            self.game.assets.fonts['small_white'].render(surf, f'x{str(item_info[1])} {(item_info[0]).replace('_', ' ')}', (surf.get_width() - self.transition, 180 - (idx * height)))
