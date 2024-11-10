from . config import config

class Item:
    def __init__(self, game, name, owner=None, amount=1):
        self.game = game
        self.name = name
        self.owner = owner
        self.amount = amount
        
        self.info = config['items'][self.name]
        self.type = self.info['type']
                    
        
        