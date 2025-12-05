from scripts.config import config

class Item:
    def __init__(self, game, name, owner=None, amount=1, tags=None):
        self.game = game
        self.name = name
        self.owner = owner
        self.amount = amount
        
        self.info = config['items'][self.name]
        self.type = self.info['type']
        
        self.tags = tags if tags else []
    
    @property
    def img(self):
        return self.game.assets.items[self.name]
    
    def add_active(self):
        self.tags.append('active')
    
    def remove_active(self):
        self.tags.remove('active')

    @property
    def is_stackable(self):
        return self.type == 'item'
    
    @property
    def is_weapon(self):
        return self.type == 'weapon'
    
    @property
    def is_consumeable(self):
        return self.type == 'consumeable'
    
    @property
    def is_tagged(self, tag): # checks if the item has a specific tag
        return tag in self.tags
    
def create_item(game, name, owner, amount=1, tags=[]):
    return Item(game, name, owner, amount, tags)
                    
        
        