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
        
    def is_tagged(self, tag): # checks if the item has a specific tag
        return tag in self.tags
                    
        
        