import scripts.pgtools as pt
from scripts.config import config

class Input(pt.Input):
    def __init__(self, render_scale, input_map=None):
        render_scale = config['window']['render_scale']
        input_map = config['input']
        super().__init__(render_scale, input_map)