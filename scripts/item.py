from . config import config

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

    def is_stackable(self):
        return self.type == 'item'
    
    def is_tagged(self, tag): # checks if the item has a specific tag
        return tag in self.tags
    
def create_item(game, name, owner, amount=1, tags=[]):
    return Item(game, name, owner, amount, tags)
                    
        
        