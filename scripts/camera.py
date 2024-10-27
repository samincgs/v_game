

class Camera:
    def __init__(self, game):
        self.game = game
        self.true_pos = [0, 0]
        self.target_pos = [0, 0]
        self.rate = 0.3
        self.tracked_entity = None
        
    def update(self):
        pass