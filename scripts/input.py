import scripts.pgtools as pt
from scripts.config import config

class Input(pt.Input):
    def __init__(self, game, render_scale, input_map=None):
        self.game = game
        input_map = config['input']
        super().__init__(render_scale, input_map)
        
    def update(self):
        self.render_scale = self.game.window.render_scale[0]
        super().update()