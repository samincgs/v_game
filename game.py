import scripts.pgtools as pt

from scripts.window import Window
from scripts.assets import Assets
from scripts.world import World
from scripts.renderer import Renderer
 
class Game: 
    def __init__(self): 
        self.window = Window(self)
        self.input = pt.Input(self.window.render_scale)
        self.assets = Assets()
        self.renderer = Renderer(self) 
        self.world = World(self)
        
    def run(self): 
        while True: 
            self.input.update()
            self.world.update()
            self.renderer.render()
            self.window.create()

if __name__ == '__main__':
    Game().run() 